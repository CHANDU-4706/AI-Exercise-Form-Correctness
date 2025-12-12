import cv2
import numpy as np

class Visualizer:
    def __init__(self):
        pass

    def draw_feedback(self, img, feedback_text, color=(0, 255, 0)):
        """Draws feedback text on the image."""
        cv2.putText(img, feedback_text, (50, 50), 
                    cv2.FONT_HERSHEY_PLAIN, 2, color, 3)

    def draw_counter(self, img, count):
        """Draws the rep counter."""
        cv2.rectangle(img, (0, 0), (150, 150), (255, 255, 255), cv2.FILLED)
        cv2.putText(img, str(int(count)), (30, 100), 
                    cv2.FONT_HERSHEY_DUPLEX, 3, (0, 0, 0), 5)
    
    def draw_angle(self, img, p1, p2, p3, angle):
        """Draws the angle at the joint."""
        # p2 is the vertex
        cv2.putText(img, str(int(angle)), (p2[0] - 20, p2[1] - 20),
                    cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 255), 2)
