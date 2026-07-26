# 🌿 AgriVision – AI-Powered Potato Disease Detection

AgriVision is an AI-powered potato leaf disease detection system that combines **Deep Learning**, **Computer Vision**, **FastAPI**, and **Flutter** to provide real-time disease identification and treatment recommendations.

The system allows users to upload or capture an image of a potato leaf, detects the disease using a Convolutional Neural Network (CNN), estimates disease severity, and recommends appropriate treatment steps.

---

# Features

- AI-based potato leaf disease detection
- Detects:
  - Healthy
  - Early Blight
  - Late Blight
- Disease severity estimation
- Confidence score prediction
- Medicine recommendation
- Dosage recommendation
- Step-by-step treatment guidance
- Camera support
- Gallery image upload
- Responsive Flutter mobile application
- FastAPI REST API backend
- Web deployment
- Android APK deployment

---

# Tech Stack

## Machine Learning

- TensorFlow
- Keras
- CNN (Convolutional Neural Network)
- OpenCV
- NumPy
- Pillow

## Backend

- FastAPI
- Uvicorn
- Python

## Mobile Application

- Flutter
- Dart
- HTTP Package
- Image Picker

## Deployment

- Render (Backend API)
- Flutter Release APK

---

# Model Performance

| Metric | Value |
|---------|---------|
| Accuracy | **96.8%** |
| Classes | Healthy, Early Blight, Late Blight |

<img width="434" height="158" alt="Screenshot 2026-07-24 162313" src="https://github.com/user-attachments/assets/d9a91e9e-6932-49fc-82ea-9c602f989f9f" />
<img width="513" height="323" alt="Screenshot 2026-07-24 162259" src="https://github.com/user-attachments/assets/e3a11d2b-f163-4e12-af4b-000f63b15b0e" />



---

# Project Architecture

```
                Potato Leaf Image
                        │
                        ▼
             Flutter Mobile Application
                        │
                        ▼
                FastAPI REST API
                        │
                        ▼
           TensorFlow CNN Prediction
                        │
        ┌───────────────┼────────────────┐
        │               │                │
        ▼               ▼                ▼
 Disease Prediction  Confidence   Severity Analysis
        │
        ▼
 Medicine + Dosage + Treatment Steps
```

---

# Screenshots

## Home Screen

<img width="540" height="1208" alt="image" src="https://github.com/user-attachments/assets/c2f214a4-93be-48e8-9887-80e3c5ac6264" />

<img width="540" height="1208" alt="image" src="https://github.com/user-attachments/assets/f75811d3-f51f-49b8-b218-7a8309c7170a" />

## Disease Prediction & Treatment Recommendation

<img width="540" height="1208" alt="image" src="https://github.com/user-attachments/assets/1b8a9d21-af85-48c0-8d01-b25c3ad4ec5e" />




---

# Web Application

The project is also available as a web application.

### Live Website

https://agrivision-yt0e.onrender.com/

ScreenShots:

<img width="959" height="539" alt="Screenshot 2026-07-26 141449" src="https://github.com/user-attachments/assets/6ed00e9c-d2a5-43af-a2db-3c6f5fae52ad" />
<img width="957" height="539" alt="Screenshot 2026-07-26 141457" src="https://github.com/user-attachments/assets/3bdcabfc-45fd-4ef5-9efb-86a342d3c323" />
<img width="950" height="537" alt="Screenshot 2026-07-26 141527" src="https://github.com/user-attachments/assets/9ad207bf-b593-45c1-851e-bd02a3475a7e" />
<img width="926" height="528" alt="Screenshot 2026-07-26 141532" src="https://github.com/user-attachments/assets/da6be535-f0f3-4dac-a084-b0e4fd8f45a6" />




---

# Mobile Application

The Flutter application communicates with the deployed FastAPI backend for disease prediction.

### Features

- Capture image using camera
- Select image from gallery
- Real-time prediction
- Treatment recommendation
- Responsive UI

APK available in GitHub Releases.

---

# Backend API

### Live API

https://agrivision-api-osv9.onrender.com

### Swagger Documentation

https://agrivision-api-osv9.onrender.com/docs

---

# API Endpoint

## POST

```
/predict
```

### Parameters

```
file : Image
language : English
```

### Response

```json
{
  "prediction": "...",
  "disease_name": "...",
  "confidence": 99.98,
  "severity": 7.63,
  "severity_level": "...",
  "medicine": "...",
  "dosage": "...",
  "steps": [
    "...",
    "..."
  ]
}
```

---

# Local Installation

## Clone Repository

```bash
git clone https://github.com/yourusername/AgriVision.git
```

```
cd AgriVision
```

---

# Backend Setup

```
pip install -r requirements.txt
```

Run

```
uvicorn main:app --reload
```

Server

```
http://127.0.0.1:8000
```

Swagger

```
http://127.0.0.1:8000/docs
```

---

# Flutter Setup

```
cd agrivision_app
```

```
flutter pub get
```

Run

```
flutter run
```

Build APK

```
flutter build apk --release
```

APK Location

```
build/app/outputs/flutter-apk/app-release.apk
```

---

# Folder Structure

```
AgriVision
│
├── Backend
│   ├── main.py
│   ├── model.keras
│   ├── predict.py
│   ├── requirements.txt
│
├── Flutter App
│   ├── lib
│   ├── android
│   ├── ios
│   └── pubspec.yaml
│
├── Dataset
│
├── README.md
```

---

# Future Improvements

- Offline inference
- Multi-language UI
- Additional crop disease detection
- Prediction history
- User authentication
- Cloud database integration
- iOS deployment

---

# Deployment

## Web Deployment

Backend deployed on Render.

Frontend (web interface) deployed on Render.

## Mobile Deployment

Flutter Release APK generated for Android devices.

The application communicates with the deployed FastAPI backend using HTTPS.

---

# Note

The backend is deployed on Render's free tier. The first request after a period of inactivity may experience a short delay due to service cold starts.

---

# Author

**Arya Bhat**

Computer Science Engineering (AI & ML)

GitHub:
https://github.com/arya0527

LinkedIn:
linkedin.com/in/arya-bhat-b9279a290

---

# License

This project is developed for educational and research purposes.
