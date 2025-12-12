from abc import ABC, abstractmethod

class BaseExercise(ABC):
    def __init__(self, name):
        self.name = name
        self.counter = 0
        self.stage = None
        self.feedback = "Generic Exercise"

    @abstractmethod
    def calculate_metrics(self, landmarks):
        """
        Calculate necessary angles and metrics from landmarks.
        """
        pass

    @abstractmethod
    def check_form(self, landmarks):
        """
        Evaluate form based on metrics.
        Returns bool indicating if form is correct, and updates self.feedback.
        """
        pass
    
    def get_feedback(self):
        return self.feedback
    
    def get_counter(self):
        return self.counter
