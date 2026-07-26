import 'package:flutter_test/flutter_test.dart';
import 'package:agrivision_app/main.dart';

void main() {
  testWidgets('AgriVision App UI smoke test', (WidgetTester tester) async {
    // Build our app and trigger a frame.
    await tester.pumpWidget(const AgriVisionApp());

    // Verify AppBar Title
    expect(find.text('AgriVision'), findsOneWidget);

    // Verify Subtitle and Info text is rendered
    expect(find.text('AI Powered Potato Disease Detection'), findsOneWidget);
    expect(
      find.text('Upload or capture a potato leaf image to detect diseases using AI.'),
      findsOneWidget,
    );

    // Verify Gallery and Camera buttons exist
    expect(find.text('Gallery'), findsOneWidget);
    expect(find.text('Camera'), findsOneWidget);

    // Verify the main Detect button is shown
    expect(find.text('Detect Disease'), findsOneWidget);
  });
}
