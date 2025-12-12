import numpy as np
from .base_exercise import BaseExercise
from ..geometry_utils import calculate_angle, EMASmoother

class BicepCurl(BaseExercise):
    def __init__(self):
        super().__init__("Bicep Curl")
    def __init__(self):
        super().__init__("Bicep Curl")
        self.stage = "down"
        self.smoother = EMASmoother(alpha=0.5)

    def calculate_metrics(self, landmarks):
        # MediaPipe Landmarks: 11=L_Shoulder, 13=L_Elbow, 15=L_Wrist
        # For simplicity, we track the LEFT arm by default or should track both.
        # Let's track the LEFT arm for this MVP.
        
        # Get coordinates
        shoulder = [landmarks[11].x, landmarks[11].y]
        elbow = [landmarks[13].x, landmarks[13].y]
        wrist = [landmarks[15].x, landmarks[15].y]
        
        angle = calculate_angle(shoulder, elbow, wrist)
        
        # Rule 2: Upper Arm stability (prevent swinging elbow forward)
        # Angle at Shoulder (Hip-Shoulder-Elbow)
        # 0 deg = arm down, 90 deg = arm forward
        upper_arm_angle = calculate_angle(hip, shoulder, elbow)
        
        # Smoothing
        angle = self.smoother.update(angle)
        # Note: We should probably smooth upper_arm_angle too, but for now we'll use raw or simple smoothing if we had another smoother.
        # Let's just return raw for checking drastic movement, or usage same smoother if appropriate (but it tracks state).
        # Better to add a second smoother in init if we want clean data.
        
        return angle, upper_arm_angle

    def check_form(self, landmarks):
        # Robustness: Check visibility
        if landmarks[11].visibility < 0.5 or landmarks[13].visibility < 0.5 or landmarks[15].visibility < 0.5:
             self.feedback = "Low Visibility"
             return False

        angle, upper_arm_angle = self.calculate_metrics(landmarks)
        
        # Logic for counter and feedback
        if angle > 160:
            self.stage = "down"
            self.feedback = "Good Extension"
        if angle < 30 and self.stage == "down":
            self.stage = "up"
            self.counter += 1
            self.feedback = "Good Curl"
        
        # Real-time feedback for range of motion
        if self.stage == "up" and angle > 30 and angle < 160:
             self.feedback = "Lower Slowly"
        
        # Rule 2 Feedback: Elbow Drift
        # If upper arm moves too much forward (> 30 degrees) while curling, it's a swing
        if upper_arm_angle > 35:
            self.feedback = "Keep Elbows Back/Still"
             
        return True
