import numpy as np
from .base_exercise import BaseExercise
from ..geometry_utils import calculate_angle, EMASmoother

class Squat(BaseExercise):
    def __init__(self):
        super().__init__("Squat")
        self.stage = "up"
        self.hip_smoother = EMASmoother(alpha=0.5)
        self.knee_smoother = EMASmoother(alpha=0.5)

    def calculate_metrics(self, landmarks):
        # Track angles for Squat
        # 1. Hip Angle (Shoulder-Hip-Knee): Determines back inclination/hip flexion
        # 2. Knee Angle (Hip-Knee-Ankle): Determines depth
        
        # Use LEFT side for MVP
        shoulder = [landmarks[11].x, landmarks[11].y]
        hip = [landmarks[23].x, landmarks[23].y]
        knee = [landmarks[25].x, landmarks[25].y]
        ankle = [landmarks[27].x, landmarks[27].y]
        
        # 1. Hip Angle (Trunk vs Thigh) - Good for depth/squeeze
        hip_angle = calculate_angle(shoulder, hip, knee)
        
        # 2. Knee Angle (Thigh vs Shin) - Depth
        knee_angle = calculate_angle(hip, knee, ankle)
        
        # 3. Back Inclination (Shoulder-Hip vs Vertical)
        # We simulate a point straight up from hip to measure inclination
        vertical_point = [hip[0], hip[1] - 0.5] # Point directly above hip
        back_inclination = calculate_angle(vertical_point, hip, shoulder)
        
        hip_angle = self.hip_smoother.update(hip_angle)
        knee_angle = self.knee_smoother.update(knee_angle)
        
        return hip_angle, knee_angle, back_inclination

    def check_form(self, landmarks):
        # Robustness
        if landmarks[23].visibility < 0.5 or landmarks[25].visibility < 0.5 or landmarks[27].visibility < 0.5:
             self.feedback = "Legs Not Visible"
             return False

        hip_angle, knee_angle, back_inclination = self.calculate_metrics(landmarks)
        
        # Logic
        # Standing: Knee angle ~170+
        # Squat: Knee angle < 90 (parallel or below)
        
        if knee_angle > 160:
            self.stage = "up"
            self.feedback = "Stand Tall"
            
        if knee_angle < 100 and self.stage == "up":
            self.feedback = "Good Depth!"
            if knee_angle < 90:
                self.stage = "down"
                self.counter += 1
        elif knee_angle < 140 and self.stage == "up":
             self.feedback = "Go Lower!"
             
        # Back form check (heuristic)
        # If hip angle is too acute, it means leaning too forward
        # Back form check
        # If back inclination is too high (leaning forward too much), angle increases/decreases?
        # Vertical is 0. Leaning forward = Angle increases.
        # Wait, calculate_angle(vertical, hip, shoulder):
        # If shoulder is directly above hip, angle is 0.
        # If shoulder is forward (x decreases if facing left? unpredictable).
        # Let's relying on `hip_angle` (Shoulder-Hip-Knee) is safer for purely "relative" body shape.
        # But `back_inclination` is good if we know orientation.
        
        # Let's stick to the existing hip_angle check but refine it.
        # A very acute hip angle (< 60) with a not-so-acute knee angle implies "Good Morning" squat (bad).
        
        if hip_angle < 60:
             self.feedback = "Keep Chest Up!"

        return True
