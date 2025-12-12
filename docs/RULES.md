# AI Trainer Implementation Report

## Overview
This system uses **Human Pose Estimation (PE)** to evaluate fitness exercises. We utilize **MediaPipe Pose** (BlazePose) for its real-time performance and 3D coordinate estimation.

## 1. Posture Rules & Logic

### Geometric Analysis
We use vector geometry to calculate angles between three keypoints (A, B, C).
Formula: `$ \theta = \arccos(\frac{\vec{BA} \cdot \vec{BC}}{|\vec{BA}| |\vec{BC}|}) $`

### rules

#### A. Bicep Curl
- **Keypoints**: Shoulder, Elbow, Wrist (Left/Right).
- **Rule 1 (Extension/Flexion)**: Elbow angle must range from > 160° (bottom) to < 30° (top).
- **Rule 2 (Elbow Drift)**: Upper arm angle (Shoulder-Elbow vs Vertical) must not exceed 35° forward. Prevents "swinging" the weight.
- **Feedback**: "Keep Elbows Back" if swinging is detected.

#### B. Lateral Raise
- **Keypoints**: Hip, Shoulder, Elbow, Wrist.
- **Rule 1 (Abduction)**: Arms raises to ~90° (parallel).
- **Rule 2 (Elbow Bend)**: Elbow angle check. Arms must remain nearly straight (> 130°).
- **Rule 3 (Wrist Height)**: Wrists should not be significantly higher than shoulders (prevents trap dominance).
- **Feedback**: "Straighten Arms", "Too High".

#### C. Squat
- **Keypoints**: Shoulder, Hip, Knee, Ankle.
- **Rule 1 (Depth)**: Knee Angle must go < 90° (parallel) for a rep.
- **Rule 2 (Chest Stability)**: Hip Angle (Shoulder-Hip-Knee) must remain open (> 60°).
- **Feedback**: "Keep Chest Up" if leaning forward too much (Good Morning squat).

#### D. Pushup
- **Keypoints**: Shoulder, Elbow, Wrist, Hip, Ankle.
- **Rule 1 (Depth)**: Elbow angle check (< 90° for down status).
- **Rule 2 (Body Line)**: Shoulder-Hip-Ankle alignment (~180°). if < 160°, pelvis is sagging.
- **Feedback**: "Fix Body Line", "Go Lower".

#### E. Shoulder Press
- **Keypoints**: Shoulder, Elbow, Wrist.
- **Rule 1 (Range of Motion)**: Starts at shoulders (< 90°), ends overhead (> 160°).
- **Feedback**: "Full Range".

## 2. Challenges & Solutions

### A. Multi-Person Scenarios
**Challenge**: MediaPipe Pose standard model detects only one person (usually the most prominent/central).
**Solution**:
1. **Confidence Thresholding**: We set `min_detection_confidence=0.7`. If the model is confused by multiple people and confidence drops, we suppress output to avoid displaying erroneous lines connecting two different people.
2. **Future Improvement**: In a production environment, we would use a lightweight object detector (YOLOv8-Nano) to crop individual people and feed crops to the Pose estimator.

### B. Jitter / Noise
**Challenge**: Keypoints shake even when static.
**Solution**: Implemented **Exponential Moving Average (EMA)** smoothing.
`$ S_t = \alpha \cdot x_t + (1-\alpha) \cdot S_{t-1} $`
This stabilizes angle readings for cleaner feedback.

### C. Occlusion
**Challenge**: Camera angle hides an arm or leg.
**Solution**: We check the `visibility` attribute of landmarks. If `< 0.5`, the system pauses analysis and alerts "Keypoints Not Visible" rather than guessing.
