import numpy as np
from .base_exercise import BaseExercise
from ..geometry_utils import calculate_angle, EMASmoother

class LateralRaise(BaseExercise):
    def __init__(self):
        super().__init__("Lateral Raise")
        self.stage = "down"
        self.smoother = EMASmoother(alpha=0.5)

    def calculate_metrics(self, landmarks):
        # Track LEFT arm: 11=L_Shoulder, 23=L_Hip, 13=L_Elbow
        # Angle at Shoulder (Hip-Shoulder-Elbow)
        
        hip = [landmarks[23].x, landmarks[23].y]
        shoulder = [landmarks[11].x, landmarks[11].y]
        elbow = [landmarks[13].x, landmarks[13].y]
        wrist = [landmarks[15].x, landmarks[15].y]
        
        angle = calculate_angle(hip, shoulder, elbow)
        angle = self.smoother.update(angle)
        
        # Rule 2: Elbow Bend (Shoulder-Elbow-Wrist)
        elbow_angle = calculate_angle(shoulder, elbow, wrist)
        
        return angle, elbow_angle, wrist, shoulder

    def check_form(self, landmarks):
         # Visibility check
        if landmarks[11].visibility < 0.5 or landmarks[23].visibility < 0.5 or landmarks[13].visibility < 0.5:
             self.feedback = "Keypoints Hidden"
             return False

        shoulder_angle, elbow_angle, wrist_coord, shoulder_coord = self.calculate_metrics(landmarks)
        
        # Lateral Raise Logic
        # Down: Arms near body (angle < 25)
        # Up: Arms parallel to floor (angle > 80)
        
        # We need a robust state machine to avoid double counting
        
        # State transitions:
        # DOWN -> UP (Count!) -> DOWN
        
        if shoulder_angle > 80 and self.stage == "down":
             self.stage = "up"
             self.counter += 1
             if shoulder_angle > 105: # Adjusted threshold
                self.feedback = "Too High! Shoulder Impingement"
             else:
                self.feedback = "Perfect Height!"
        elif shoulder_angle < 20:
             self.stage = "down"
             self.feedback = "Raise Arms"
             
        # Rule 2 Check: Elbow Bend
        # Arms should be nearly straight (150-180), not bent like a Chicken Wing (< 130)
        if elbow_angle < 130:
            self.feedback = "Straighten Arms"
            
        # Rule 3 Check: Wrist above Shoulder (common mistake leading to trap usage)
        # Note: in image coords, smaller Y is higher.
        if wrist_coord[1] < shoulder_coord[1] - 0.05: # Tolerance
             # If wrist is significantly above shoulder
             pass # Actually this is covered by "Too High", but we can be specific
             # self.feedback = "Lead with Elbows"
             
        # Backup reset logic
        if self.feedback == "Perfect Height!" and shoulder_angle < 70:
            self.feedback = "Lower Slowly"
        
        return True
