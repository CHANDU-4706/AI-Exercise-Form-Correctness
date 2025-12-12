# AI Personal Trainer - Computer Vision Form Correction

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![MediaPipe](https://img.shields.io/badge/MediaPipe-Pose-orange)
![OpenCV](https://img.shields.io/badge/OpenCV-Computer%20Vision-green)
![MLflow](https://img.shields.io/badge/MLflow-Tracking-blueviolet)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

**AI Personal Trainer** is a cutting-edge computer vision application designed to act as your virtual gym instructor. By leveraging **MediaPipe's State-of-the-Art Pose Estimation**, this system analyzes your movements for specific exercises in real-time, counts valid repetitions, and provides instant, actionable feedback to correct your form.

No wearable sensors required—just a simple webcam or video file.

---

## 🚀 Key Features

*   **Real-time Form Analysis**: Detects body keypoints at 30+ FPS (CPU/GPU).
*   **Instant Feedback**: "Keep Elbows Back", "Go Lower", "Straighten Back" – get corrected immediately.
*   **Smart Rep Counting**: Reps are only counted if the exercise form is valid (e.g., full range of motion).
*   **MLflow Integration**: Tracks your workout sessions, total reps, and performance metrics automatically.
*   **Smoothed Tracking**: Implements advanced smoothing algorithms (Exponential Moving Average) to reduce jitter and noise.

---

## 🛠️ Tech Stack

*   **Language**: Python
*   **Core Logic**: OpenCV (Image Processing), MediaPipe (Pose Estimation)
*   **Math/Geometry**: NumPy (Vector calculations for joint angles)
*   **Tracking**: MLflow (Metric logging)

---

## 🏋️ Supported Exercises

The system currently supports 5 major exercises, each with specific biomechanical rules:

1.  **Bicep Curl**: Ensures full extension and prevents elbow swinging.
2.  **Squat**: Checks for proper depth (knee angle) and back stability.
3.  **Pushup**: Monitors body alignment (no sagging) and chest depth.
4.  **Lateral Raise**: Prevents going too high (impingement risk) and checks elbow bend.
5.  **Shoulder Press**: Verifies full overhead range of motion.

> 📄 **Deep Dive**: Check [docs/RULES.md](docs/RULES.md) for the detailed logic, geometric formulas, and biomechanical rules used for each exercise.

---

## ⚙️ Installation

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/CHANDU-4706/AI-Exercise-Form-Correctness.git
    cd AI-Exercise-Form-Correctness
    ```

2.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

---

## 🏃 Usage

You can run the AI Trainer using your webcam or a pre-recorded video.

### 1. Using Webcam (Live Mode)
Run the script and specify the exercise you want to perform:
```bash
python main.py --exercise curl
```
*Available exercises:* `curl`, `squat`, `pushup`, `lateral`, `press`

### 2. Using a Video File
Analyze an existing video for form assessment:
```bash
python main.py --video "data/your_video.mp4" --exercise squat
```

---

## 📂 Project Structure

```
AI-Exercise-Form-Correctness/
├── data/                   # Sample videos
├── docs/
│   └── RULES.md            # Detailed detection logic and rules
├── src/
│   ├── exercises/          # Specific logic for each exercise (Squat, Curl, etc.)
│   ├── pose_detector.py    # MediaPipe wrapper class
│   └── visualizer.py       # UI/Drawing utilities
├── main.py                 # Entry point of the application
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation
```

## 🔮 Future Scope
- **Multi-Person Detection**: Handling class scenarios.
- **Mobile App Integration**: Deploying the model to iOS/Android using TFLite.
- **Advanced Analytics**: Long-term progress tracking dashboard.

---
*Developed by Chandu*
