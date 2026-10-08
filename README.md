# 🌿 AgriVision – AI-Powered Potato Disease Detection & Treatment Assistant

AgriVision is an **AI-powered agricultural assistance system** that combines **Deep Learning, Computer Vision, Generative AI, and Agentic AI** to detect potato leaf diseases and provide actionable treatment guidance.

The system uses a **CNN-based deep learning model** to identify potato leaf diseases and estimate disease severity. An **Agno-based multi-agent system** then uses the CNN's verified prediction and treatment information to generate a concise, farmer-friendly solution in **English or Hindi**.

> **Important design principle:** The AI agents do not replace or modify the CNN diagnosis. The CNN remains the source of truth for disease classification, confidence, and severity. Agents are responsible for reasoning over the existing result and presenting the treatment information clearly.

---

# 🚀 Key Features

### 🌱 Disease Detection
- Potato leaf disease classification using CNN
- Supports:
  - Healthy
  - Early Blight
  - Late Blight
- Confidence score prediction
- Disease severity estimation

### 🤖 Agentic AI
- Built using **Agno**
- Multi-agent architecture
- Specialized Potato Treatment Agent
- English Language Agent
- Hindi Language Agent
- Agent team-based routing
- Uses the CNN output as structured input
- Prevents agents from independently diagnosing the image
- Prevents agents from modifying CNN predictions

### 💊 Treatment Assistance
- Medicine recommendation
- Dosage information
- Treatment steps
- Severity-aware recommendations
- Farmer-friendly explanations
- Multilingual treatment guidance

### 🖼️ Explainable AI
- Grad-CAM based visual explanation
- Helps understand which regions of the leaf influenced the CNN prediction

### 🌐 Applications
- Web application
- REST API
- Android application
- Camera input
- Gallery image upload
- English/Hindi output

---

# 🧠 System Architecture

```text
                         Potato Leaf Image
                                │
                                ▼
                     ┌─────────────────────┐
                     │   Flutter / Web UI  │
                     └──────────┬──────────┘
                                │
                                ▼
                     ┌─────────────────────┐
                     │     FastAPI API     │
                     └──────────┬──────────┘
                                │
                                ▼
                     ┌─────────────────────┐
                     │   CNN Classifier    │
                     │     TensorFlow      │
                     └──────────┬──────────┘
                                │
                    ┌───────────┼────────────┐
                    │           │            │
                    ▼           ▼            ▼
                Disease     Confidence    Severity
                Prediction     Score       Analysis
                    │           │            │
                    └───────────┼────────────┘
                                │
                                ▼
                    Verified Treatment Data
                                │
                                ▼
                     ┌─────────────────────┐
                     │    Agno AI Team     │
                     └──────────┬──────────┘
                                │
                  ┌─────────────┼─────────────┐
                  │             │             │
                  ▼             ▼             ▼
             Potato Agent  English Agent  Hindi Agent
                  │             │             │
                  └─────────────┼─────────────┘
                                │
                                ▼
                  Farmer-Friendly Final Response
                                │
                                ▼
                   Medicine + Dosage + Steps
```

---

# 🔥 How AgriVision Works

AgriVision follows a **two-stage AI pipeline**.

## Stage 1 – CNN Disease Detection

The uploaded potato leaf image is processed using a TensorFlow/Keras CNN.

The CNN determines:

```text
Disease
Confidence
Severity
Severity Level
```

For example:

```json
{
    "disease_name": "Early Blight",
    "confidence": 99.8,
    "severity": 7.63,
    "severity_level": "Moderate"
}
```

The CNN prediction is treated as the **source of truth**.

The agents are explicitly instructed **not to perform another diagnosis**.

---

# Stage 2 – Agentic Treatment Reasoning

The CNN result and verified treatment information are passed to the **Agno Potato Agent**.

The Potato Agent's responsibility is to:

- Understand the existing CNN prediction
- Consider the severity
- Use the provided treatment information
- Organize the treatment steps
- Explain the solution clearly to the farmer

It does **not**:

- Re-diagnose the image
- Change the disease predicted by the CNN
- Change the CNN confidence
- Change the severity
- Invent medicines
- Invent dosages
- Generate unsupported treatment information

This separation makes the system more reliable because the **computer vision model handles diagnosis**, while the **LLM-based agent handles reasoning and communication**.

---

# 🤖 Multi-Agent Architecture

AgriVision uses **Agno** to implement an agent-based workflow.

### Potato Agent

The Potato Agent acts as the agricultural reasoning agent.

Input:

```text
CNN Prediction
Confidence
Severity
Severity Level
Verified Medicine
Verified Dosage
Verified Treatment Steps
```

Output:

```text
Concise agricultural solution
```

The agent is instructed to preserve the provided medical/agricultural information rather than inventing new values.

---

### English Agent

The English Agent converts the verified solution into a clear English response suitable for farmers.

---

### Hindi Agent

The Hindi Agent presents the same verified solution in Hindi.

---

### Language Team

The language agents are grouped into an Agno team that routes the response according to the selected language.

```text
                    Final Solution
                          │
                          ▼
                  ┌───────────────┐
                  │ Language Team │
                  └───────┬───────┘
                          │
              ┌───────────┴───────────┐
              ▼                       ▼
        English Agent             Hindi Agent
              │                       │
              ▼                       ▼
       English Response          Hindi Response
```

The language agents only change **presentation/language**, not the underlying diagnosis or treatment values.

---

# 🧠 AI / ML Pipeline

```text
Image
  │
  ▼
Image Preprocessing
  │
  ▼
CNN
  │
  ├── Disease Classification
  │
  ├── Confidence
  │
  └── Severity Estimation
          │
          ▼
   Verified Treatment Data
          │
          ▼
      Agno Agent
          │
          ▼
   Language Routing
          │
          ▼
 Farmer-Friendly Response
```

---

# 📊 Model Performance

| Metric | Value |
|---|---:|
| Accuracy | **96.8%** |
| Classes | 3 |
| Framework | TensorFlow / Keras |
| Architecture | CNN |

### Supported Classes

| Class | Description |
|---|---|
| 🟢 Healthy | Healthy potato leaf |
| 🟠 Early Blight | Early-stage fungal disease |
| 🔴 Late Blight | Late blight disease |

---

# 🔍 Explainable AI – Grad-CAM

AgriVision also uses **Grad-CAM (Gradient-weighted Class Activation Mapping)** to provide visual explanations for CNN predictions.

Grad-CAM highlights the areas of the leaf that contributed most strongly to the model's prediction.

```text
Potato Leaf
     │
     ▼
    CNN
     │
     ▼
Prediction
     │
     ▼
Grad-CAM
     │
     ▼
Highlighted Disease-Relevant Regions
```

This makes the model more interpretable instead of treating the CNN as a complete black box.

---

# 🛠️ Technology Stack

## Machine Learning

- Python
- TensorFlow
- Keras
- CNN
- OpenCV
- NumPy
- Pillow

## Generative AI / Agents

- Agno
- Groq
- LLMs
- Multi-Agent Team
- Agent Routing

## Backend

- FastAPI
- Uvicorn
- Python

## Frontend / Application

- Flutter
- Dart
- HTTP
- Image Picker

## Web Interface

- Streamlit

## Deployment

- Render
- Android APK

---

# 📱 Mobile Application

The Flutter application provides an easy interface for farmers.

### Features

- 📷 Capture leaf image using camera
- 🖼️ Select image from gallery
- 🔬 Disease detection
- 📊 Confidence score
- 🌱 Severity estimation
- 💊 Treatment recommendation
- 🌐 Language selection
- 📱 Responsive mobile UI

The Flutter application communicates with the deployed backend through HTTP/HTTPS requests.

---

# 🌐 Web Application

AgriVision is also available through a web interface.

### Live Website

[AgriVision Web Application](https://agrivision-yt0e.onrender.com/?utm_source=chatgpt.com)

The web interface allows users to:

1. Select the preferred language
2. Upload a potato leaf image
3. Run disease detection
4. View the CNN prediction
5. View confidence and severity
6. Receive AI-generated treatment guidance

---

# ⚡ Backend API

### Live API

[AgriVision API](https://agrivision-api-osv9.onrender.com?utm_source=chatgpt.com)

### Swagger Documentation

[Swagger API Documentation](https://agrivision-api-osv9.onrender.com/docs?utm_source=chatgpt.com)

---

# 🔌 API Endpoint

## `POST /predict`

### Input

```text
file      : Image
language  : English / Hindi
```

### Example Response

```json
{
  "prediction": "Early Blight",
  "disease_name": "Early Blight",
  "confidence": 99.98,
  "severity": 7.63,
  "severity_level": "Moderate",
  "medicine": "...",
  "dosage": "...",
  "steps": [
    "...",
    "..."
  ]
}
```

---

# 🔄 End-to-End Request Flow

```text
User uploads image
        │
        ▼
FastAPI receives image
        │
        ▼
Image preprocessing
        │
        ▼
CNN inference
        │
        ├── Disease
        ├── Confidence
        └── Severity
        │
        ▼
Treatment information
        │
        ▼
Agno Potato Agent
        │
        ▼
Language Team
        │
        ├── English
        └── Hindi
        │
        ▼
Final Response
        │
        ▼
User
```

---

# 📂 Project Structure

```text
AgriVision/
│
├── Backend/
│   ├── main.py
│   ├── predict.py
│   ├── model.keras
│   ├── requirements.txt
│   └── ...
│
├── Flutter App/
│   ├── lib/
│   ├── android/
│   ├── ios/
│   └── pubspec.yaml
│
├── Streamlit/
│   └── app.py
│
├── Agents/
│   ├── potato_agent.py
│   ├── language_agents.py
│   └── ...
│
├── Dataset/
│
└── README.md
```

---

# 💡 Key Engineering Decisions

### 1. CNN and LLM have separate responsibilities

The CNN is responsible for:

```text
Image → Disease + Confidence + Severity
```

The LLM agent is responsible for:

```text
CNN Result + Treatment Data → Human-Friendly Explanation
```

This prevents the LLM from becoming an uncontrolled diagnostic component.

---

### 2. Agents do not modify model predictions

If the CNN predicts:

```text
Early Blight
Confidence: 99.8%
Severity: Moderate
```

the agent must preserve those values.

It cannot change the prediction to Late Blight simply because the LLM considers it more likely.

---

### 3. Structured information is passed to the agent

Instead of asking the LLM to independently diagnose the plant, the system provides structured information such as:

```text
Disease: Early Blight
Confidence: 99.8%
Severity: Moderate
Medicine: ...
Dosage: ...
Treatment Steps: ...
```

The agent then generates the final explanation from that information.

---

### 4. Multilingual AI response

The system separates **reasoning** from **language presentation**.

```text
CNN
 ↓
Treatment Reasoning
 ↓
Verified Solution
 ↓
Language Agent
 ↓
English / Hindi
```

This makes it easier to add additional languages in the future.

---

# 📦 Local Installation

## 1. Clone Repository

```bash
git clone https://github.com/arya0527/AgriVision.git
cd AgriVision
```

---

# ⚙️ Backend Setup

Install dependencies:

```bash
pip install -r requirements.txt
```

Run FastAPI:

```bash
uvicorn main:app --reload
```

Server:

```text
http://127.0.0.1:8000
```

Swagger:

```text
http://127.0.0.1:8000/docs
```

---

# 🤖 Agent Setup

Configure the required LLM provider/API key in the environment.

Example:

```text
GROQ_API_KEY=your_api_key
```

The Agno agents can then use the configured LLM to generate the treatment explanation.

---

# 📱 Flutter Setup

Navigate to the Flutter application:

```bash
cd "Flutter App"
```

Install dependencies:

```bash
flutter pub get
```

Run:

```bash
flutter run
```

Build release APK:

```bash
flutter build apk --release
```

APK:

```text
build/app/outputs/flutter-apk/app-release.apk
```

---

# 🚀 Deployment

## Backend

The FastAPI backend is deployed using:

**Render**

The backend exposes the prediction API through HTTPS.

## Web Application

The web interface is deployed using:

**Render**

## Mobile Application

The Android application is packaged as a Flutter release APK.

---

# ⚠️ Deployment Note

The backend is hosted on Render's free tier.

Because the service can enter an inactive state, the first request after a period of inactivity may experience a short delay due to a **cold start**.

---

# 🔮 Future Improvements

- [ ] Offline/on-device CNN inference
- [ ] More crop disease classes
- [ ] Additional crop support
- [ ] More Indian regional languages
- [ ] Prediction history
- [ ] User authentication
- [ ] Cloud database
- [ ] Farmer-specific recommendations
- [ ] iOS deployment
- [ ] Better disease severity estimation
- [ ] Model monitoring and evaluation
- [ ] RAG-based agricultural knowledge system
- [ ] Retrieval-based treatment verification
- [ ] Agent evaluation and guardrails

---

# 🎯 What This Project Demonstrates

AgriVision demonstrates practical experience with:

- **Computer Vision**
- **CNNs**
- **Deep Learning**
- **Image Classification**
- **Grad-CAM / Explainable AI**
- **Severity Estimation**
- **FastAPI**
- **REST APIs**
- **Flutter**
- **Generative AI**
- **LLM Agents**
- **Agno**
- **Multi-Agent Systems**
- **Agent Routing**
- **Prompt Engineering**
- **Multilingual AI**
- **Model + LLM integration**
- **Cloud Deployment**

---

# 👨‍💻 Author

### Arya Bhat

**Computer Science Engineering – Artificial Intelligence & Machine Learning**

GitHub:  
[Arya Bhat – GitHub](https://github.com/arya0527?utm_source=chatgpt.com)

LinkedIn:  
[Arya Bhat – LinkedIn](https://linkedin.com/in/arya-bhat-b9279a290?utm_source=chatgpt.com)

---

# 📜 License

This project is developed for **educational and research purposes**.
