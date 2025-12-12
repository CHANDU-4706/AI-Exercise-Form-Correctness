import numpy as np
from .base_exercise import BaseExercise
from ..geometry_utils import calculate_angle, EMASmoother

class Pushup(BaseExercise):
    def __init__(self):
        super().__init__("Pushup")
        self.stage = "up"
        self.smoother = EMASmoother(alpha=0.5)

    def calculate_metrics(self, landmarks):
        # Keypoints (Left side for MVP)
        shoulder = [landmarks[11].x, landmarks[11].y]
        elbow = [landmarks[13].x, landmarks[13].y]
        wrist = [landmarks[15].x, landmarks[15].y]
        hip = [landmarks[23].x, landmarks[23].y]
        ankle = [landmarks[27].x, landmarks[27].y]
        
        # 1. Elbow Angle (Depth)
        elbow_angle = calculate_angle(shoulder, elbow, wrist)
        
        # 2. Body Alignment (Shoulder-Hip-Ankle) - Should be ~180
        body_angle = calculate_angle(shoulder, hip, ankle)
        
        elbow_angle = self.smoother.update(elbow_angle)
        
        return elbow_angle, body_angle

    def check_form(self, landmarks):
        if landmarks[11].visibility < 0.5 or landmarks[13].visibility < 0.5 or landmarks[23].visibility < 0.5:
             self.feedback = "Not Visible"
             return False

        elbow_angle, body_angle = self.calculate_metrics(landmarks)
        
        # Form Logic
        # Body Line Check
        if body_angle < 160:
            self.feedback = "Fix Body Line (Sagging)"
        elif body_angle > 200: # Example logic for piking (though angle definition matters)
             self.feedback = "Lower Hips"
             
        # Rep Logic
        # Down: Elbow < 90
        # Up: Elbow > 160
        
        if elbow_angle > 160:
            self.stage = "up"
            if self.feedback != "Fix Body Line (Sagging)":
                 self.feedback = "Start Position"
                 
        if elbow_angle < 90 and self.stage == "up":
            self.stage = "down"
            self.counter += 1
            self.feedback = "Good Pushup!"
        elif elbow_angle < 120 and self.stage == "up":
             self.feedback = "Go Lower"
             
        return True
