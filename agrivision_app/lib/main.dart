import 'dart:io';
import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import 'services/api_service.dart';

void main() {
  runApp(const AgriVisionApp());
}

/// The core application widget for AgriVision.
/// Sets up the Material 3 design system with light and dark themes.
class AgriVisionApp extends StatelessWidget {
  const AgriVisionApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'AgriVision',
      themeMode: ThemeMode.system,
      // Light Green Theme (Material 3)
      theme: ThemeData(
        useMaterial3: true,
        colorScheme: ColorScheme.fromSeed(
          seedColor: const Color(0xFF2E7D32), // Forest Green
          primary: const Color(0xFF2E7D32),
          secondary: const Color(0xFF4CAF50),
          brightness: Brightness.light,
        ),
        cardTheme: CardThemeData(
          elevation: 2,
          shadowColor: Colors.black.withValues(alpha: 0.15),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(16),
          ),
          color: Colors.white,
        ),
        elevatedButtonTheme: ElevatedButtonThemeData(
          style: ElevatedButton.styleFrom(
            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
            padding: const EdgeInsets.symmetric(vertical: 14, horizontal: 20),
          ),
        ),
      ),
      // Dark Green Theme (Material 3)
      darkTheme: ThemeData(
        useMaterial3: true,
        colorScheme: ColorScheme.fromSeed(
          seedColor: const Color(0xFF2E7D32), // Forest Green
          primary: const Color(0xFF81C784),
          secondary: const Color(0xFF66BB6A),
          brightness: Brightness.dark,
        ),
        cardTheme: CardThemeData(
          elevation: 1,
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(16),
          ),
          color: Colors.grey.shade900,
        ),
      ),
      home: const HomePage(),
    );
  }
}

/// Home screen containing all user interaction elements.
class HomePage extends StatefulWidget {
  const HomePage({super.key});

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  final ImagePicker _picker = ImagePicker();
  File? _selectedImage;
  bool _isLoading = false;
  PotatoDiseaseResult? _result;

  /// Trigger gallery picker to select a leaf image.
  Future<void> _pickImage() async {
    try {
      final XFile? image = await _picker.pickImage(
        source: ImageSource.gallery,
        imageQuality: 85,
      );

      if (image != null) {
        setState(() {
          _selectedImage = File(image.path);
          // UX requirement: Clear previous prediction when a new image is selected.
          _result = null;
        });
      }
    } catch (e) {
      _showErrorSnackBar("Failed to select image from gallery: ${e.toString()}");
    }
  }

  /// Trigger system camera to capture a leaf image.
  Future<void> _captureImage() async {
    try {
      final XFile? image = await _picker.pickImage(
        source: ImageSource.camera,
        imageQuality: 85,
      );

      if (image != null) {
        setState(() {
          _selectedImage = File(image.path);
          // UX requirement: Clear previous prediction when a new image is selected.
          _result = null;
        });
      }
    } catch (e) {
      _showErrorSnackBar("Failed to capture image using camera: ${e.toString()}");
    }
  }

  /// Uploads selected leaf image and processes potato disease prediction.
  Future<void> _detectDisease() async {
    if (_selectedImage == null || _isLoading) return;

    setState(() {
      _isLoading = true;
      _result = null;
    });

    try {
      final result = await ApiService.predictDisease(_selectedImage!);
      setState(() {
        _result = result;
      });
      _showSuccessSnackBar("Analysis completed successfully!");
    } catch (e) {
      // Handles network errors, status codes, and server errors gracefully.
      _showErrorSnackBar(e.toString().replaceAll("HttpException: ", ""));
    } finally {
      setState(() {
        _isLoading = false;
      });
    }
  }

  /// Reset the app screen back to original state.
  void _clearState() {
    setState(() {
      _selectedImage = null;
      _result = null;
    });
  }

  /// Helper to display failure messages inside a Material SnackBar.
  void _showErrorSnackBar(String message) {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Row(
          children: [
            const Icon(Icons.error_outline, color: Colors.white),
            const SizedBox(width: 12),
            Expanded(
              child: Text(
                message,
                style: const TextStyle(color: Colors.white, fontWeight: FontWeight.w500),
              ),
            ),
          ],
        ),
        backgroundColor: Theme.of(context).colorScheme.error,
        behavior: SnackBarBehavior.floating,
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
        margin: const EdgeInsets.all(16),
        duration: const Duration(seconds: 4),
      ),
    );
  }

  /// Helper to display success messages inside a Material SnackBar.
  void _showSuccessSnackBar(String message) {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Row(
          children: [
            const Icon(Icons.check_circle_outline, color: Colors.white),
            const SizedBox(width: 12),
            Expanded(
              child: Text(
                message,
                style: const TextStyle(color: Colors.white, fontWeight: FontWeight.w500),
              ),
            ),
          ],
        ),
        backgroundColor: Colors.green.shade700,
        behavior: SnackBarBehavior.floating,
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
        margin: const EdgeInsets.all(16),
        duration: const Duration(seconds: 2),
      ),
    );
  }

  /// Determine matching color code matching target severity level.
  Color _getSeverityColor(String severityLevel) {
    switch (severityLevel.toLowerCase()) {
      case 'low':
        return Colors.green.shade600;
      case 'medium':
        return Colors.orange.shade700;
      case 'high':
      case 'critical':
        return Colors.red.shade700;
      default:
        return Colors.grey.shade600;
    }
  }

  /// Determine severity warning icon based on intensity level.
  IconData _getSeverityIcon(String severityLevel) {
    switch (severityLevel.toLowerCase()) {
      case 'low':
        return Icons.check_circle_outline_rounded;
      case 'medium':
        return Icons.warning_amber_rounded;
      case 'high':
      case 'critical':
        return Icons.gpp_bad_rounded;
      default:
        return Icons.help_outline_rounded;
    }
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final colorScheme = theme.colorScheme;

    return Scaffold(
      appBar: AppBar(
        title: const Text(
          "AgriVision",
          style: TextStyle(fontWeight: FontWeight.bold, letterSpacing: 0.5),
        ),
        centerTitle: true,
        backgroundColor: colorScheme.primary,
        foregroundColor: colorScheme.onPrimary,
        elevation: 0,
        actions: [
          IconButton(
            icon: const Icon(Icons.info_outline),
            onPressed: () {
              showAboutDialog(
                context: context,
                applicationName: "AgriVision",
                applicationVersion: "1.0.0",
                applicationIcon: Icon(
                  Icons.eco_rounded,
                  color: colorScheme.primary,
                  size: 40,
                ),
                children: [
                  const Text(
                    "AgriVision uses AI predictions to identify and diagnose "
                    "potato leaf diseases quickly. Simply take a snapshot or load "
                    "a picture to receive immediate treatments and advice.",
                  ),
                ],
              );
            },
          ),
        ],
      ),
      body: SafeArea(
        child: SingleChildScrollView(
          physics: const BouncingScrollPhysics(),
          padding: const EdgeInsets.symmetric(horizontal: 20.0, vertical: 16.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              // Header Section
              Card(
                elevation: 0,
                color: colorScheme.primaryContainer.withValues(alpha: 0.2),
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(16),
                  side: BorderSide(color: colorScheme.primaryContainer.withValues(alpha: 0.4), width: 1.5),
                ),
                child: Padding(
                  padding: const EdgeInsets.all(20.0),
                  child: Column(
                    children: [
                      Icon(
                        Icons.eco_rounded,
                        color: colorScheme.primary,
                        size: 80,
                      ),
                      const SizedBox(height: 12),
                      Text(
                        "AI Powered Potato Disease Detection",
                        textAlign: TextAlign.center,
                        style: theme.textTheme.titleMedium?.copyWith(
                          fontWeight: FontWeight.bold,
                          color: colorScheme.onPrimaryContainer,
                          fontSize: 19,
                        ),
                      ),
                      const SizedBox(height: 8),
                      Text(
                        "Upload or capture a potato leaf image to detect diseases using AI.",
                        textAlign: TextAlign.center,
                        style: theme.textTheme.bodyMedium?.copyWith(
                          color: colorScheme.onPrimaryContainer.withValues(alpha: 0.8),
                        ),
                      ),
                    ],
                  ),
                ),
              ),
              const SizedBox(height: 20),

              // Leaf Image Container Section
              Text(
                "Potato Leaf Image",
                style: theme.textTheme.titleMedium?.copyWith(fontWeight: FontWeight.bold),
              ),
              const SizedBox(height: 8),
              Container(
                height: 250,
                decoration: BoxDecoration(
                  borderRadius: BorderRadius.circular(16),
                  border: Border.all(
                    color: colorScheme.outline.withValues(alpha: 0.2),
                    width: 1.5,
                  ),
                  color: theme.brightness == Brightness.light
                      ? Colors.grey.shade50
                      : Colors.grey.shade900,
                ),
                child: ClipRRect(
                  borderRadius: BorderRadius.circular(14),
                  child: _selectedImage != null
                      ? Stack(
                          fit: StackFit.expand,
                          children: [
                            Image.file(
                              _selectedImage!,
                              fit: BoxFit.cover,
                            ),
                            // Quick clear float action button
                            Positioned(
                              top: 10,
                              right: 10,
                              child: Container(
                                decoration: BoxDecoration(
                                  color: Colors.black.withValues(alpha: 0.6),
                                  shape: BoxShape.circle,
                                ),
                                child: IconButton(
                                  icon: const Icon(Icons.close_rounded, color: Colors.white, size: 20),
                                  tooltip: "Clear Image",
                                  onPressed: _isLoading ? null : _clearState,
                                ),
                              ),
                            ),
                          ],
                        )
                      : Center(
                          child: Padding(
                            padding: const EdgeInsets.all(20.0),
                            child: Column(
                              mainAxisAlignment: MainAxisAlignment.center,
                              children: [
                                Icon(
                                  Icons.image_search_rounded,
                                  size: 60,
                                  color: colorScheme.outline.withValues(alpha: 0.5),
                                ),
                                const SizedBox(height: 12),
                                Text(
                                  "No image selected",
                                  style: theme.textTheme.bodyMedium?.copyWith(
                                    fontWeight: FontWeight.w600,
                                    color: colorScheme.outline,
                                  ),
                                ),
                                const SizedBox(height: 4),
                                Text(
                                  "Pick from Gallery or use the Camera to capture",
                                  textAlign: TextAlign.center,
                                  style: theme.textTheme.bodySmall?.copyWith(
                                    color: colorScheme.outline.withValues(alpha: 0.7),
                                  ),
                                ),
                              ],
                            ),
                          ),
                        ),
                ),
              ),
              const SizedBox(height: 20),

              // Capture and Library Select Action Panel
              Row(
                children: [
                  Expanded(
                    child: OutlinedButton.icon(
                      onPressed: _isLoading ? null : _pickImage,
                      icon: const Icon(Icons.photo_library_outlined),
                      label: const Text("Gallery"),
                      style: OutlinedButton.styleFrom(
                        padding: const EdgeInsets.symmetric(vertical: 14),
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(12),
                        ),
                      ),
                    ),
                  ),
                  const SizedBox(width: 12),
                  Expanded(
                    child: OutlinedButton.icon(
                      onPressed: _isLoading ? null : _captureImage,
                      icon: const Icon(Icons.camera_alt_outlined),
                      label: const Text("Camera"),
                      style: OutlinedButton.styleFrom(
                        padding: const EdgeInsets.symmetric(vertical: 14),
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(12),
                        ),
                      ),
                    ),
                  ),
                ],
              ),
              const SizedBox(height: 16),

              // Run Diagnosis Core Button
              FilledButton.icon(
                onPressed: (_selectedImage == null || _isLoading) ? null : _detectDisease,
                icon: _isLoading
                    ? SizedBox(
                        width: 20,
                        height: 20,
                        child: CircularProgressIndicator(
                          strokeWidth: 2.5,
                          color: colorScheme.onPrimary,
                        ),
                      )
                    : const Icon(Icons.psychology_rounded),
                label: Text(
                  _isLoading ? "Analyzing leaf..." : "Detect Disease",
                  style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
                ),
                style: FilledButton.styleFrom(
                  padding: const EdgeInsets.symmetric(vertical: 16),
                  backgroundColor: colorScheme.primary,
                  foregroundColor: colorScheme.onPrimary,
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(12),
                  ),
                ),
              ),
              const SizedBox(height: 24),

              // Results Presentation Area
              if (_result != null) ...[
                Text(
                  "Detection Result",
                  style: theme.textTheme.titleMedium?.copyWith(fontWeight: FontWeight.bold),
                ),
                const SizedBox(height: 10),
                Card(
                  clipBehavior: Clip.antiAlias,
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.stretch,
                    children: [
                      // Header Severity Strip
                      Container(
                        color: _getSeverityColor(_result!.severityLevel).withValues(alpha: 0.12),
                        padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
                        child: Row(
                          children: [
                            Icon(
                              _getSeverityIcon(_result!.severityLevel),
                              color: _getSeverityColor(_result!.severityLevel),
                            ),
                            const SizedBox(width: 8),
                            Text(
                              "Severity: ${_result!.severityLevel}",
                              style: theme.textTheme.labelLarge?.copyWith(
                                fontWeight: FontWeight.bold,
                                color: _getSeverityColor(_result!.severityLevel),
                              ),
                            ),
                            const Spacer(),
                            Container(
                              padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                              decoration: BoxDecoration(
                                color: _getSeverityColor(_result!.severityLevel),
                                borderRadius: BorderRadius.circular(20),
                              ),
                              child: Text(
                                "Score: ${_result!.severity.toStringAsFixed(2)}",
                                style: const TextStyle(
                                  color: Colors.white,
                                  fontSize: 12,
                                  fontWeight: FontWeight.bold,
                                ),
                              ),
                            ),
                          ],
                        ),
                      ),
                      Padding(
                        padding: const EdgeInsets.all(16.0),
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            // Condition & Confidence Header Row
                            Row(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                Expanded(
                                  child: Column(
                                    crossAxisAlignment: CrossAxisAlignment.start,
                                    children: [
                                      Text(
                                        "DISEASE NAME",
                                        style: theme.textTheme.bodySmall?.copyWith(
                                          color: colorScheme.outline,
                                          fontWeight: FontWeight.bold,
                                          letterSpacing: 0.5,
                                        ),
                                      ),
                                      const SizedBox(height: 4),
                                      Text(
                                        _result!.diseaseName,
                                        style: theme.textTheme.titleLarge?.copyWith(
                                          fontWeight: FontWeight.bold,
                                          color: colorScheme.primary,
                                        ),
                                      ),
                                    ],
                                  ),
                                ),
                                const SizedBox(width: 8),
                                Column(
                                  crossAxisAlignment: CrossAxisAlignment.end,
                                  children: [
                                    Text(
                                      "CONFIDENCE",
                                      style: theme.textTheme.bodySmall?.copyWith(
                                        color: colorScheme.outline,
                                        fontWeight: FontWeight.bold,
                                        letterSpacing: 0.5,
                                      ),
                                    ),
                                    const SizedBox(height: 4),
                                    Text(
                                      "${_result!.confidence.toStringAsFixed(2)}%",
                                      style: theme.textTheme.titleMedium?.copyWith(
                                        fontWeight: FontWeight.bold,
                                        color: colorScheme.secondary,
                                      ),
                                    ),
                                  ],
                                ),
                              ],
                            ),
                            const SizedBox(height: 12),

                            // Confidence bar
                            ClipRRect(
                              borderRadius: BorderRadius.circular(4),
                              child: LinearProgressIndicator(
                                value: _result!.confidence / 100.0,
                                backgroundColor: colorScheme.primary.withValues(alpha: 0.12),
                                color: colorScheme.primary,
                                minHeight: 8,
                              ),
                            ),
                            const SizedBox(height: 20),
                            const Divider(),
                            const SizedBox(height: 12),

                            // Medicine & Dosage row items
                            Row(
                              children: [
                                Expanded(
                                  child: _buildInfoItem(
                                    context,
                                    icon: Icons.healing_rounded,
                                    label: "Medicine",
                                    value: _result!.medicine,
                                  ),
                                ),
                                Container(
                                  width: 1,
                                  height: 50,
                                  color: theme.brightness == Brightness.light
                                      ? Colors.grey.shade200
                                      : Colors.grey.shade800,
                                  margin: const EdgeInsets.symmetric(horizontal: 12),
                                ),
                                Expanded(
                                  child: _buildInfoItem(
                                    context,
                                    icon: Icons.opacity_rounded,
                                    label: "Dosage",
                                    value: _result!.dosage,
                                  ),
                                ),
                              ],
                            ),
                            const SizedBox(height: 20),
                            const Divider(),
                            const SizedBox(height: 16),

                            // Treatment Steps list heading
                            Row(
                              children: [
                                Icon(Icons.list_alt_rounded, color: colorScheme.primary, size: 22),
                                const SizedBox(width: 8),
                                Text(
                                  "Treatment Steps",
                                  style: theme.textTheme.titleMedium?.copyWith(
                                    fontWeight: FontWeight.bold,
                                    color: colorScheme.primary,
                                  ),
                                ),
                              ],
                            ),
                            const SizedBox(height: 12),

                            // Display Treatment Steps
                            if (_result!.steps.isEmpty)
                              Text(
                                "No treatment steps recorded for this diagnosis.",
                                style: theme.textTheme.bodyMedium?.copyWith(
                                  fontStyle: FontStyle.italic,
                                  color: colorScheme.outline,
                                ),
                              )
                            else
                              ...List.generate(
                                _result!.steps.length,
                                (index) => Padding(
                                  padding: const EdgeInsets.only(bottom: 10.0),
                                  child: Row(
                                    crossAxisAlignment: CrossAxisAlignment.start,
                                    children: [
                                      Padding(
                                        padding: const EdgeInsets.only(top: 3.0),
                                        child: Container(
                                          decoration: BoxDecoration(
                                            color: colorScheme.primary.withValues(alpha: 0.12),
                                            shape: BoxShape.circle,
                                          ),
                                          padding: const EdgeInsets.all(4),
                                          child: Icon(
                                            Icons.arrow_forward_rounded,
                                            size: 10,
                                            color: colorScheme.primary,
                                          ),
                                        ),
                                      ),
                                      const SizedBox(width: 12),
                                      Expanded(
                                        child: Text(
                                          _result!.steps[index],
                                          style: theme.textTheme.bodyMedium?.copyWith(
                                            height: 1.35,
                                          ),
                                        ),
                                      ),
                                    ],
                                  ),
                                ),
                              ),
                          ],
                        ),
                      ),
                    ],
                  ),
                ),
              ],
            ],
          ),
        ),
      ),
    );
  }

  /// Quick helper to render a localized column pair.
  Widget _buildInfoItem(
    BuildContext context, {
    required IconData icon,
    required String label,
    required String value,
  }) {
    final theme = Theme.of(context);
    final colorScheme = theme.colorScheme;
    return Row(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Icon(icon, color: colorScheme.primary, size: 28),
        const SizedBox(width: 10),
        Expanded(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                label.toUpperCase(),
                style: theme.textTheme.bodySmall?.copyWith(
                  color: colorScheme.outline,
                  fontWeight: FontWeight.bold,
                  fontSize: 10,
                  letterSpacing: 0.5,
                ),
              ),
              const SizedBox(height: 4),
              Text(
                value,
                style: theme.textTheme.bodyMedium?.copyWith(
                  fontWeight: FontWeight.bold,
                  height: 1.2,
                ),
              ),
            ],
          ),
        ),
      ],
    );
  }
}