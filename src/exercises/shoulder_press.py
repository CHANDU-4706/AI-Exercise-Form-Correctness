import numpy as np
from .base_exercise import BaseExercise
from ..geometry_utils import calculate_angle, EMASmoother

class ShoulderPress(BaseExercise):
    def __init__(self):
        super().__init__("Shoulder Press")
        self.stage = "down"
        self.smoother = EMASmoother(alpha=0.5)

    def calculate_metrics(self, landmarks):
        # Keypoints (Left side checking)
        # Ideally check BOTH sides for symmetry, but MVP uses Left
        shoulder = [landmarks[11].x, landmarks[11].y]
        elbow = [landmarks[13].x, landmarks[13].y]
        wrist = [landmarks[15].x, landmarks[15].y]
        hip = [landmarks[23].x, landmarks[23].y]
        
        # 1. Elbow Angle (ROM)
        elbow_angle = calculate_angle(shoulder, elbow, wrist)
        
        # 2. Shoulder Alignment (Elbow vs Shoulder verticality)
        # Check if elbows are too far forward?
        
        elbow_angle = self.smoother.update(elbow_angle)
        return elbow_angle

    def check_form(self, landmarks):
        if landmarks[11].visibility < 0.5 or landmarks[13].visibility < 0.5:
             self.feedback = "Not Visible"
             return False

        elbow_angle = self.calculate_metrics(landmarks)
        
        # Logic
        # Start (Down): Elbows bent ~90 or less (or at shoulder level)
        # Finish (Up): Arms extended overhead > 160
        
        if elbow_angle < 90:
            self.stage = "down"
            self.feedback = "Push Up!"
            
        if elbow_angle > 160 and self.stage == "down":
            self.stage = "up"
            self.counter += 1
            self.feedback = "Good Press!"
        
        return True
