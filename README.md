# AI Trainer - Form Correctness Detection

This computer vision project uses MediaPipe Pose to analyze exercise form in real-time. It provides immediate feedback on posture and repetitions for Bicep Curls, Lateral Raises, and Squats.

## Features
- **Real-time Pose Estimation**: Uses MediaPipe for high-performance keypoint tracking.
- **Form Correction**: Geometric algorithms analyze joint angles to provide "Good/Bad" feedback.
- **Robustness**: Handles missing keypoints, jitter (smoothing), and basic occlusion.
- **Exercises Supported**:
  - **Bicep Curl**: Monitors elbow extension/flexion range of motion.
  - **Lateral Raise**: Monitors arm height (impingement check) and elbow bend.
  - **Squat**: Monitors depth (knee angle) and back posture (chest up).
  - **Pushup**: Monitors depth and body alignment (sagging hips).
  - **Shoulder Press**: Monitors full overhead range of motion.

## Installation

1. Clone the repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the main script with a webcam (default) or video file:

```bash
# Webcam (Default: Bicep Curl)
python main.py --exercise curl

# Video File
python main.py --video "data/sample_squat.mp4" --exercise squat

# Options for --exercise
# - curl
# - lateral
# - squat
# - pushup
# - press
```

## Structure
- `src/`: Core source code.
- `src/exercises/`: Logic for specific exercises.
- `geometry_utils.py`: Math helpers and smoothing.
- `pose_detector.py`: MediaPipe wrapper.

## Documentation
See `docs/REPORT.md` for detailed explanation of rules, logic, and challenges handling.
