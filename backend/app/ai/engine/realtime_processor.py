import time

from app.ai.hand_tracking.hand_detector import HandDetector
from app.ai.gesture_recognition.landmark_converter import LandmarkConverter
from app.ai.ml.inference.predictor import Predictor
from app.ai.temporal.temporal_buffer import TemporalBuffer
from app.ai.temporal.stable_detector import StableGestureDetector
from app.ai.utils.fps_counter import FPSCounter
from app.ai.validation.frame_validator import FrameValidator


class RealTimeGestureProcessor:

    def __init__(self):

        self.hand_detector = HandDetector(max_num_hands=1)

        self.landmark_converter = LandmarkConverter()

        self.predictor = Predictor()

        self.temporal_buffer = TemporalBuffer(max_frames=30)

        self.stable_detector = StableGestureDetector(
            required_stable_frames=5,
            confidence_threshold=0.60
        )

        self.fps_counter = FPSCounter()

        self.frame_validator = FrameValidator()
        
        self.gesture_start_time = None

    # =====================================================
    # Process Webcam Frame
    # =====================================================

    def process(self, frame, expected_gesture=None):

        start_time = time.perf_counter()

        # -----------------------------------------------
        # Update FPS
        # -----------------------------------------------

        self.fps_counter.update()

        # -----------------------------------------------
        # Detect Hands
        # -----------------------------------------------

        detection = self.hand_detector.detect(frame)

        # -----------------------------------------------
        # Get Landmarks
        # -----------------------------------------------

        landmarks = None

        if detection["hand_count"] > 0:
            landmarks = detection["landmarks"][0]

        # -----------------------------------------------
        # Validate Frame
        # -----------------------------------------------

        validation = self.frame_validator.validate(
            landmarks=landmarks,
            hand_count=detection["hand_count"],
            person_count=detection["person_count"],
            body_visible=detection["body_visible"]
        )
        if self.gesture_start_time is None:
            self.gesture_start_time = time.perf_counter()

        # -----------------------------------------------
        # Default Response
        # -----------------------------------------------

        response = {
            "prediction": None,
            "confidence": 0.0,
            "stable": False,
            "stable_frames": 0,
            "temporal_sequence_length": 0,
            "validation": validation
        }
        completion_time = time.perf_counter() - self.gesture_start_time

        assessment = self.assessment_engine.evaluate(
               expected_gesture=expected_gesture,
    prediction=stable_result["prediction"],
    confidence=stable_result["confidence"],
    validation=validation,
    stable_frames=stable_result["stable_frames"],
    unstable_frames=stable_result["unstable_frames"],
    completion_time=completion_time,
    gesture_stability=stable_result["gesture_stability"]
)
        response["assessment"] = assessment
        self.gesture_start_time = None

        # -----------------------------------------------
        # Stop if frame is invalid
        # -----------------------------------------------

        if not validation["valid"]:

            response["performance"] = {
                "fps": round(self.fps_counter.get_fps(), 2),
                "latency_ms": round(
                    (time.perf_counter() - start_time) * 1000,
                    2
                )
            }

            return response

        # -----------------------------------------------
        # Temporal Buffer
        # -----------------------------------------------

        self.temporal_buffer.add_frame(landmarks)

        # -----------------------------------------------
        # Prediction
        # -----------------------------------------------

        prediction_result = self.predictor.predict(landmarks)

        prediction = prediction_result["prediction"]
        confidence = prediction_result["confidence"]

        # -----------------------------------------------
        # Stable Gesture Detection
        # -----------------------------------------------

        stable_result = self.stable_detector.update(
            prediction,
            confidence
        )

        # -----------------------------------------------
        # Update Response
        # -----------------------------------------------

        response.update({
            "prediction": stable_result["prediction"],
            "confidence": confidence,
            "stable": stable_result["stable"],
            "stable_frames": stable_result["stable_frames"],
            "temporal_sequence_length": self.temporal_buffer.size()
        })

        # -----------------------------------------------
        # Performance
        # -----------------------------------------------

        response["performance"] = {
            "fps": round(self.fps_counter.get_fps(), 2),
            "latency_ms": round(
                (time.perf_counter() - start_time) * 1000,
                2
            )
        }

        return response