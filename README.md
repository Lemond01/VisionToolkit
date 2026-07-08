# VisionToolkit - Focus Monitor 👁️

An AI-powered attention monitoring system built with **Computer Vision** that uses a webcam to analyze eye movement, detect distractions, and help users maintain focus during study or work sessions.

The goal of this project is to explore how Computer Vision technologies can be applied to create practical productivity tools using accessible hardware such as a standard webcam.

---

# 📌 Features

✅ **Real-time Face Detection**  
Uses MediaPipe Face Mesh to detect facial landmarks and track relevant facial features.

✅ **Eye Gaze Tracking**  
Analyzes iris position to estimate where the user is looking and determine attention direction.

✅ **Eye Closure Detection (EAR)**  
Uses the Eye Aspect Ratio algorithm to detect prolonged eye closure.

✅ **Automatic User Calibration**  
Creates a personalized baseline according to each user's natural position in front of the camera.

✅ **Smart Distraction Alerts**  
Triggers configurable alerts when the user remains distracted for a specific amount of time.

✅ **Focus Statistics**
Tracks session information such as:

- Total session time.
- Focused time.
- Distracted time.
- Number of distractions detected.

✅ **Real-Time Visual Interface**
Displays the current attention state directly on the camera feed.

---

# 🎯 Project Motivation

Maintaining concentration during long computer sessions can be challenging due to:

- Mobile devices.
- External distractions.
- Frequent attention switching.
- Visual fatigue.

VisionToolkit explores how Computer Vision can help users become more aware of their focus habits through a non-invasive monitoring system.

---

# 🧠 How It Works

The system follows this pipeline:

```
Webcam
  |
  ↓
Image Capture
  |
  ↓
MediaPipe Face Mesh
  |
  ↓
Facial Landmark Extraction
  |
  ├── Iris Tracking 👁️
  |
  ├── Eye Aspect Ratio (EAR)
  |
  ↓
Attention Analysis
  |
  ↓
Focus State Decision
  |
  ↓
Alert System
```

---

# 🛠️ Technologies

## Programming Language

🐍 **Python 3.12**

---

## Main Libraries

### OpenCV

Used for:

- Webcam access.
- Image processing.
- Real-time visualization.

https://opencv.org/

---

### MediaPipe

Used for:

- Face landmark detection.
- Iris tracking.
- Facial feature extraction.

https://developers.google.com/mediapipe

---

### NumPy

Used for:

- Mathematical calculations.
- Data processing.

https://numpy.org/

---

### Audio Processing Library

Used for:

- Sound alerts.
- Notification management.

---

# 🏗️ Architecture

The project follows **SOLID principles** and a modular architecture where each component has a specific responsibility.

Example structure:

```
VisionToolkit/

├── main.py

├── config.py

├── core/
│   ├── attention_monitor.py
│   ├── calibration.py
│   └── state.py

├── detectors/
│   ├── face_detector.py
│   ├── gaze_detector.py
│   └── eye_detector.py

├── services/
│   ├── camera_service.py
│   ├── alert_service.py
│   └── focus_service.py

├── ui/
│   └── overlay.py

└── assets/
    └── alert.wav
```

---

# 🚀 Installation

## 1. Clone the repository

```bash
git clone <repository-url>

cd VisionToolkit
```

---

## 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it:

### Windows

```bash
.venv\Scripts\activate
```

---

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

# ▶️ Running the Project

Start the application:

```bash
python main.py
```

When launched:

1. The webcam starts.
2. The calibration process begins.
3. The system starts monitoring attention.

---

# 🎮 Controls

| Key | Action |
|---|---|
| Q | Exit application |
| R | Recalibrate user |
| M | Change visualization mode |

---

# ⚙️ Configuration

Main parameters can be adjusted in:

```
config.py
```

Example:

```python
DISTRACTION_TIME = 5

GAZE_HORIZONTAL_MARGIN = 0.18

GAZE_VERTICAL_MARGIN = 0.12
```

This allows sensitivity adjustments according to each user's behavior.

---

# 📊 System States

The system can detect different attention states:

🟢 **FOCUSED**

The user is maintaining attention.

🟡 **WARNING**

The user's gaze moved outside the expected area.

🔴 **DISTRACTED**

The distraction exceeded the configured time limit and an alert is triggered.

---

# 📚 Learning Outcomes

This project explores:

- Computer Vision fundamentals.
- Image processing.
- Face landmarks.
- Eye tracking.
- Software architecture.
- SOLID principles.
- Modular application design.
- Iterative development.

---

# 👨‍💻 Author

**Sergio Hernández García**

Software Engineering Student

Interests:

- Computer Vision
- Game Development
- Full Stack Development
- UX/UI Design

---

# 📄 License

This project was created for educational purposes and experimentation with Computer Vision technologies.