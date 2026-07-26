import 'dart:async';
import 'dart:convert';
import 'dart:io';
import 'package:http/http.dart' as http;

/// Model class representing the potato disease detection result.
class PotatoDiseaseResult {
  final String prediction;
  final String diseaseName;
  final double confidence;
  final double severity;
  final String severityLevel;
  final String medicine;
  final String dosage;
  final List<String> steps;

  PotatoDiseaseResult({
    required this.prediction,
    required this.diseaseName,
    required this.confidence,
    required this.severity,
    required this.severityLevel,
    required this.medicine,
    required this.dosage,
    required this.steps,
  });

  /// Factory method to safely parse a JSON map to PotatoDiseaseResult.
  factory PotatoDiseaseResult.fromJson(Map<String, dynamic> json) {
    return PotatoDiseaseResult(
      prediction: json['prediction'] as String? ?? 'Unknown',
      diseaseName: json['disease_name'] as String? ?? 'Unknown',
      confidence: (json['confidence'] as num?)?.toDouble() ?? 0.0,
      severity: (json['severity'] as num?)?.toDouble() ?? 0.0,
      severityLevel: json['severity_level'] as String? ?? 'Unknown',
      medicine: json['medicine'] as String? ?? 'N/A',
      dosage: json['dosage'] as String? ?? 'N/A',
      steps: (json['steps'] as List<dynamic>?)
              ?.map((e) => e.toString())
              .toList() ??
          [],
    );
  }
}

class ApiService {
  static const String baseUrl = "https://agrivision-api-osv9.onrender.com";

  /// Sends a potato leaf image to the backend prediction API and returns the parsed result.
  static Future<PotatoDiseaseResult> predictDisease(File imageFile) async {
    try {
      final request = http.MultipartRequest(
        'POST',
        Uri.parse('$baseUrl/predict?language=English'),
      );

      request.files.add(
        await http.MultipartFile.fromPath(
          'file',
          imageFile.path,
        ),
      );

      // Perform request with a 30 second timeout.
      final streamedResponse = await request.send().timeout(
        const Duration(seconds: 120),
      );

      final responseBody = await streamedResponse.stream.bytesToString();

      if (streamedResponse.statusCode == 200) {
        final Map<String, dynamic> json = jsonDecode(responseBody);
        return PotatoDiseaseResult.fromJson(json);
      } else {
        String errorMsg = "Prediction failed.";
        try {
          final errorJson = jsonDecode(responseBody);
          if (errorJson is Map && errorJson.containsKey('error')) {
            errorMsg = errorJson['error'].toString();
          } else if (errorJson is Map && errorJson.containsKey('message')) {
            errorMsg = errorJson['message'].toString();
          }
        } catch (_) {}
        throw HttpException("$errorMsg (Status Code: ${streamedResponse.statusCode})");
      }
    } on SocketException {
      throw const HttpException("Network error: Please check your internet connection.");
    } on TimeoutException {
      throw const HttpException("Connection timeout. The server took too long to respond.");
    } catch (e) {
      if (e is HttpException) rethrow;
      throw HttpException("Request failed: ${e.toString()}");
    }
  }
}