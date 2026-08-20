import time
import numpy as np


class MotionMetrics:
    """
    Calculates motion-based gesture assessment metrics.

    Metrics:
    - Gesture stability
    - Landmark movement
    - Invalid frame count
    - Average confidence
    - Time taken
    """

    def __init__(self):

        self.landmark_history = []

        self.confidence_history = []

        self.invalid_frames = 0

        self.start_time = None

        self.end_time = None

    # ---------------------------------------
    # Add landmark frame
    # ---------------------------------------

    def add_landmarks(self, landmarks):

        if landmarks is not None and self.start_time is None:
            self.start_time = time.time()

        if landmarks is None:
            self.invalid_frames += 1
            return

        self.landmark_history.append(landmarks)

        self.end_time = time.time()

    # ---------------------------------------
    # Add confidence
    # ---------------------------------------

    def add_confidence(self, confidence):

        if confidence is None:
            self.invalid_frames += 1
            return

        confidence = float(confidence)

        # Normalize if confidence is already in %
        if confidence > 1:
            confidence /= 100

        confidence = float(np.clip(confidence, 0, 1))

        self.confidence_history.append(confidence)

    # ---------------------------------------
    # Gesture Stability
    # ---------------------------------------

    def calculate_stability(self):
        if len(self.landmark_history) < 2:
            return 0.0
        movements = []

        for i in range(1, len(self.landmark_history)):

            previous = np.array(
                self.landmark_history[i - 1],
                dtype=float
            )

            current = np.array(
                self.landmark_history[i],
                dtype=float
            )

            try:
                movement = np.linalg.norm(current - previous)
                movements.append(movement)

            except Exception:
                continue

        if not movements:
            return 0.0

        average_motion = np.mean(movements)

        stability = 100 - (average_motion * 100)

        stability = float(np.clip(stability, 0, 100))

        return round(stability, 2)

    # ---------------------------------------
    # Average Confidence (%)
    # ---------------------------------------

    def average_confidence(self):

        if len(self.confidence_history) == 0:
            return 0.0

        return round(
            float(np.mean(self.confidence_history) * 100),
            2
        )

    # ---------------------------------------
    # Invalid Frames
    # ---------------------------------------

    def get_invalid_frames(self):

        return self.invalid_frames

    # ---------------------------------------
    # Time Taken
    # ---------------------------------------

    def calculate_time_taken(self):

        if (
            self.start_time is None
            or
            self.end_time is None
        ):
            return 0.0

        return round(
            self.end_time - self.start_time,
            2
        )

    # ---------------------------------------
    # Complete Metrics
    # ---------------------------------------

    def get_metrics(self):

        return {

            "gesture_stability":
                self.calculate_stability(),

            "average_confidence":
                self.average_confidence(),

            "invalid_frames":
                self.invalid_frames,

            "time_taken":
                self.calculate_time_taken(),

            "frames_analyzed":
                len(self.landmark_history)

        }

    # ---------------------------------------
    # Reset
    # ---------------------------------------

    def reset(self):

        self.landmark_history.clear()

        self.confidence_history.clear()

        self.invalid_frames = 0

        self.start_time = None

        self.end_time = None