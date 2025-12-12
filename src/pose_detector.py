import mediapipe as mp
import cv2
import numpy as np

class PoseDetector:
    def __init__(self, mode=False, complexity=1, smooth_landmarks=True, 
                 enable_segmentation=False, smooth_segmentation=True,
                 detection_confidence=0.5, tracking_confidence=0.5):
        
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(
            static_image_mode=mode,
            model_complexity=complexity,
            smooth_landmarks=smooth_landmarks,
            enable_segmentation=enable_segmentation,
            smooth_segmentation=smooth_segmentation,
            min_detection_confidence=detection_confidence,
            min_tracking_confidence=tracking_confidence
        )
        self.mp_drawing = mp.solutions.drawing_utils

    def find_pose(self, img, draw=True):
        """
        Processes the image and finds the pose. 
        Returns the image with drawings (if enabled) and the results object.
        """
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(img_rgb)
        
        if self.results.pose_landmarks:
            if draw:
                self.mp_drawing.draw_landmarks(
                    img, 
                    self.results.pose_landmarks, 
                    self.mp_pose.POSE_CONNECTIONS
                )
        return img, self.results

    def find_position(self, img, draw=True):
        """
        Extracts landmarks into a list format [id, x, y, visibility]
        """
        lm_list = []
        if self.results.pose_landmarks:
            h, w, c = img.shape
            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                cx, cy = int(lm.x * w), int(lm.y * h)
                lm_list.append([id, cx, cy, lm.visibility])
                if draw:
                    cv2.circle(img, (cx, cy), 5, (255, 0, 0), cv2.FILLED)
        return lm_list
