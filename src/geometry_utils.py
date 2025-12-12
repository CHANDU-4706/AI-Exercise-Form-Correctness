import numpy as np
import math

def calculate_angle(a, b, c):
    """
    Calculates the angle at point b given three points a, b, c.
    Points are (x, y) tuples or identifiable objects with x, y attributes.
    Returns angle in degrees.
    """
    # Robustness: Check for missing points
    if a is None or b is None or c is None:
        return 0.0

    # Convert to numpy arrays for easier math
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)

    # Calculate vectors BA and BC
    ba = a - b
    bc = c - b

    # Robustness: Check for zero length vectors (overlapping points)
    norm_ba = np.linalg.norm(ba)
    norm_bc = np.linalg.norm(bc)

    if norm_ba == 0 or norm_bc == 0:
        return 0.0

    # Calculate cosine of angle
    cosine_angle = np.dot(ba, bc) / (norm_ba * norm_bc)
    
    # Robustness: Clip to handle floating point errors outside domain [-1, 1]
    cosine_angle = np.clip(cosine_angle, -1.0, 1.0)
    
    angle = np.arccos(cosine_angle)
    return np.degrees(angle)

def calculate_distance(a, b):
    """Euclidean distance between two points."""
    if a is None or b is None:
        return 0.0
    a = np.array(a)
    b = np.array(b)
    return np.linalg.norm(a - b)

class EMASmoother:
    """
    Exponential Moving Average Smoother to reduce jitter in keypoint detection.
    """
    def __init__(self, alpha=0.5):
        self.alpha = alpha
        self.value = None

    def update(self, new_value):
        if new_value is None:
            return self.value
            
        if self.value is None:
            self.value = new_value
        else:
            self.value = self.alpha * new_value + (1 - self.alpha) * self.value
        return self.value
