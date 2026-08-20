import time
import cv2
from app.ai.engine.ai_engine import AIEngine
from app.learning.practice_session import PracticeSession

from app.ai.temporal.temporal_buffer import TemporalBuffer
from app.learning.motion_metrics import MotionMetrics
from app.assessment.sign_score import SignScoreCalculator

from app.ai.hand_tracking.hand_detector import HandDetector
from app.ai.gesture_recognition.landmark_converter import LandmarkConverter
from app.ai.ml.inference.feature_converter import FeatureConverter
from app.ai.temporal.stable_detector import StableGestureDetector
from app.ai.validation.frame_validator import FrameValidator
from app.services.learner.learner_profile_service import LearnerProfileService

class LivePractice:
    """
    Connects AI prediction with learning workflow.

    Responsibilities
    ----------------
    • Capture webcam frames
    • Validate frames
    • Store temporal sequence
    • Predict gestures
    • Track motion metrics
    • Generate assessment score
    """

    def __init__(self, letter, student_id):
        self.expected_letter = letter.upper()
        self.student_id = str(student_id)
        self.profile_service = LearnerProfileService()


        # AI Engine
        self.ai_engine = AIEngine()

        # Learning Session
        self.session = PracticeSession(self.expected_letter)

        # Temporal Buffer
        self.temporal_buffer = TemporalBuffer(
            max_frames=30
        )

        # Motion Metrics
        self.motion_metrics = MotionMetrics()

        # Assessment Score
        self.score_calculator = SignScoreCalculator()

        # Frame Validator
        self.frame_validator = FrameValidator()
        self.stable_detector = StableGestureDetector(
    required_stable_frames=5
)

        # Timing
        self.gesture_start_time = None

        # Latest Result
        self.last_correct = False

        # Hand Detector
        self.detector = HandDetector(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
        )

    # ==========================================================
    # Start Practice
    # ==========================================================



    def start_practice(self):
        self.temporal_buffer.clear()
        self.motion_metrics.reset()
        self.stable_detector.reset()
        self.gesture_start_time = time.time()
        self.last_correct = False
        return {
        "message": "Practice started",
        "expected_letter": self.expected_letter
    }
    # ==========================================================
    # Store Temporal Frame
    # ==========================================================

    def store_temporal_frame(self, frame):

        try:

            detection = self.detector.detect(frame)

            frame = detection["frame"]

            hand_count = detection["hand_count"]

            person_count = detection["person_count"]

            body_visible = detection["body_visible"]

            hands = detection["landmarks"]

            validation = self.frame_validator.validate(
                landmarks=hands[0] if hand_count > 0 else None,
                hand_count=hand_count,
                person_count=person_count,
                body_visible=body_visible
            )

            # Invalid frame
            if not validation["valid"]:

                self.motion_metrics.add_landmarks(None)

                return {
                    "success": False,
                    "validation": validation
                }

            # First detected hand
            landmarks = hands[0]

            # Convert to model format
            model_landmarks = LandmarkConverter.to_model_format(
                landmarks
            )

            # Convert to feature vector
            features = FeatureConverter.to_feature_vector(
                model_landmarks
            )

            # Store in temporal buffer
            self.temporal_buffer.add_frame(
                features
            )

            # Update motion metrics
            self.motion_metrics.add_landmarks(
                model_landmarks
            )

            return {
                "success": True,
                "validation": validation,
                "frame": frame
            }

        except Exception as e:

            print("Temporal Error:", e)

            self.motion_metrics.add_landmarks(None)

            return {
                "success": False,
                "validation": {
                    "valid": False,
                    "reason": "PROCESSING_ERROR"
                }
            }
            # ==========================================================
    # Process Frame
    # ==========================================================

    def process_frame(self, frame):
        print("\n========================")
        print("LivePractice object:", id(self))
        print("Stable Detector object:", id(self.stable_detector))
        print("========================")

        # Store frame in temporal buffer
        temporal_result = self.store_temporal_frame(frame)

        if not temporal_result["success"]:

            self.motion_metrics.add_confidence(None)

            return {
                "success": False,
                "validation": temporal_result["validation"],
                "motion_metrics": self.motion_metrics.get_metrics()
            }

        # Run prediction
        result = self.ai_engine.predict_image(frame)

        if not result.success:

            self.motion_metrics.add_confidence(None)

            return {
                "success": False,
                "message": result.message,
                "motion_metrics": self.motion_metrics.get_metrics()
            }

        prediction = result.prediction
        confidence = result.confidence
        stable_result = self.stable_detector.update(
    prediction,
    confidence
)
        print("\n===== STABLE DETECTOR =====")
        print(stable_result)
        print("===========================\n")
        if stable_result.get("stable", False):
            prediction = stable_result["prediction"]
            confidence = stable_result["confidence"]
            if stable_result.get("new_stable", False):
                evaluation = self.session.evaluate_prediction(
            prediction,
            confidence
        )
                self.last_correct = evaluation["correct"]
                self.profile_service.update_after_attempt(
            student_id=self.student_id,
            alphabet=self.expected_letter,
            predicted=prediction,
            confidence=confidence,
            correct=self.last_correct
        )
        # Evaluate prediction
        

        metrics = self.motion_metrics.get_metrics()

        assessment = self.get_assessment_score()

        return {

            "success": True,

            "expected": self.expected_letter,

            "prediction": prediction,

            "confidence": confidence,

            "correct": self.last_correct,

            "attempt": self.session.attempts,

            "accuracy": self.session.get_accuracy(),

            "temporal_buffer_size": self.temporal_buffer.size(),

            "motion_metrics": metrics,

            "assessment_score": assessment,
            "stable_prediction": stable_result

        }

    # ==========================================================
    # Assessment Score
    # ==========================================================

    def get_assessment_score(self):

        metrics = self.motion_metrics.get_metrics()

        time_taken = 0

        if self.gesture_start_time:

            time_taken = (
                time.time() - self.gesture_start_time
            )

        score = self.score_calculator.calculate(

            correct=self.last_correct,

            confidence=metrics.get(
                "average_confidence",
                0
            ),

            stability=metrics.get(
                "gesture_stability",
                0
            ),

            time_taken=time_taken

        )

        score["time_taken"] = round(
            time_taken,
            2
        )

        score["invalid_frames"] = metrics.get(
            "invalid_frames",
            0
        )

        score["frames_analyzed"] = metrics.get(
            "frames_analyzed",
            0
        )

        return score
        # ==========================================================
    # Get Temporal Sequence
    # ==========================================================

    def get_temporal_sequence(self):
        """
        Returns the complete temporal sequence stored
        inside the temporal buffer.
        """

        return self.temporal_buffer.get_sequence()

    # ==========================================================
    # Clear Temporal Buffer
    # ==========================================================

    def clear_temporal_buffer(self):

        self.stable_detector.reset()

        self.temporal_buffer.clear()

        self.motion_metrics.reset()

        self.gesture_start_time = None

        self.last_correct = False

    # ==========================================================
    # Change Expected Letter
    # ==========================================================

    def next_letter(self, letter):
        self.stable_detector.reset()

        self.expected_letter = letter.upper()

        self.session.change_letter(
            self.expected_letter
        )

        self.temporal_buffer.clear()

        self.motion_metrics.reset()

        self.gesture_start_time = time.time()

        self.last_correct = False

        return {

            "next_letter": self.expected_letter

        }

    # ==========================================================
    # Practice Summary
    # ==========================================================

    def get_summary(self):

        summary = self.session.summary()

        summary["motion_metrics"] = (
            self.motion_metrics.get_metrics()
        )

        summary["temporal_sequence_length"] = (
            len(
                self.temporal_buffer.get_sequence()
            )
        )

        summary["assessment_score"] = (
            self.get_assessment_score()
        )

        return summary


# =====================================================
# Manual Test Runner
# =====================================================
if __name__ == "__main__":

    print("\nStarting Live Practice Test...\n")

    practice = LivePractice(
        "A",
        "test_student"
    )

    print(practice.start_practice())

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("ERROR: Could not open webcam.")
        exit()

    print("\nWebcam started.")
    print("Show the letter A.")
    print("Press Q to quit.\n")

    while True:

        ret, frame = cap.read()

        if not ret:
            print("ERROR: Could not read webcam frame.")
            break

        result = practice.process_frame(frame)

        print("\nRESULT:")
        print(result)

        cv2.imshow(
            "SignSync Live Practice",
            frame
        )

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

    print("\n==============================")
    print("FINAL PRACTICE SUMMARY")
    print("==============================")

    print(
        practice.get_summary()
    )