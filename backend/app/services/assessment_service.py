from datetime import datetime
import uuid

# ============================================================
# CORE SERVICES
# ============================================================
from app.reports.report_service import ReportService
from app.content.lesson_service import LessonService
from app.services.session_service import SessionService
from app.services.gesture_service import GestureService

from app.ai.temporal.frame_detection_service import (
    FrameDetectionService,
)

# ============================================================
# FEEDBACK & ASSESSMENT
# ============================================================
from app.feedback.feedback_engine import FeedbackEngine
from app.feedback.personalized_feedback import PersonalizedFeedback
from app.assessment.sign_score import SignScoreCalculator

# ============================================================
# LEARNER
# ============================================================
from app.services.learner.learner_profile_service import (
    LearnerProfileService,
)
from app.analytics.recommendation_engine import (
    RecommendationEngine,
)

# ============================================================
# ASSESSMENT HISTORY & ANALYTICS
# ============================================================
from app.assessment.assessment_history import AssessmentHistory
from app.analytics.learning_state import LearningState
from app.analytics.error_analysis_service import (
    ErrorAnalysisService,
)
from app.services.dashboard.dashboard_service import (
    DashboardService,
)

# ============================================================
# VALIDATION
# ============================================================
from app.ai.validation.frame_validator import FrameValidator

# ============================================================
# TEMPORAL / RUNTIME COMPONENTS
# ============================================================
from app.ai.temporal.temporal_buffer import TemporalBuffer
from app.ai.temporal.stable_detector import (
    StableGestureDetector,
)
from app.ai.temporal.stability_calculator import (
    StabilityCalculator,
)
from app.learning.motion_metrics import MotionMetrics
from app.ai.performance.performance_monitor import (
    PerformanceMonitor,
)

# ============================================================
# PRACTICE
# ============================================================
from app.learning.practice_queue import PracticeQueue
from app.analytics.attempt_tracker import AttemptTracker


class AssessmentService:
    """
    ============================================================
    Assessment Service
    ============================================================
    """

    def __init__(self):

        # =====================================================
        # CORE SERVICES
        # =====================================================

        self.lesson_service = LessonService()

        self.session_service = SessionService()

        self.gesture_service = GestureService()

        self.frame_detection_service = (
            FrameDetectionService()
        )

        # =====================================================
        # FEEDBACK & ASSESSMENT
        # =====================================================

        self.feedback_engine = FeedbackEngine()

        self.personalized_feedback = (
            PersonalizedFeedback()
        )

        self.score_calculator = SignScoreCalculator()

        self.assessment_history = AssessmentHistory()

        self.report_service = ReportService(
            self.assessment_history
        )

        # =====================================================
        # LEARNER
        # =====================================================

        self.learner_profile_service = (
            LearnerProfileService()
        )

        self.recommendation_engine = (
            RecommendationEngine()
        )

        # =====================================================
        # LEARNING STATE & ERROR ANALYSIS
        # =====================================================

        self.learning_state = LearningState()

        self.error_analysis_service = (
            ErrorAnalysisService(
                self.assessment_history
            )
        )

        # =====================================================
        # DASHBOARD
        # =====================================================

        self.dashboard_service = DashboardService(
            learner_profile_service=
                self.learner_profile_service,

            recommendation_engine=
                self.recommendation_engine,

            assessment_history=
                self.assessment_history,

            learning_state=
                self.learning_state,
        )

        # =====================================================
        # FRAME VALIDATION & PRACTICE QUEUE
        # =====================================================

        self.frame_validator = FrameValidator()

        self.practice_queue = PracticeQueue()

        # =====================================================
        # TRACKERS & RUNTIME COMPONENTS
        # =====================================================

        self.student_trackers = {}

        self.temporal_buffers = {}

        self.stable_detectors = {}

        self.stability_calculators = {}

        self.motion_metrics = {}

        self.performance_monitors = {}

    # ============================================================
    # TRACKER
    # ============================================================

    def get_tracker(self, student_id):

        if student_id not in self.student_trackers:

            self.student_trackers[student_id] = (
                AttemptTracker(student_id)
            )

        return self.student_trackers[student_id]

    # ============================================================
    # CLEAN PREDICTION
    # ============================================================

    def clean_prediction(self, prediction):

        if prediction is None:

            return "UNKNOWN"

        return str(
            prediction
        ).strip().upper()

    # ============================================================
    # NORMALIZE CONFIDENCE
    # ============================================================

    def normalize_confidence(self, confidence):

        try:

            confidence = float(confidence)

        except (TypeError, ValueError):

            return 0.0

        if confidence > 1:

            confidence /= 100.0

        return round(
            max(
                0.0,
                min(
                    1.0,
                    confidence
                )
            ),
            4
        )

    # ============================================================
    # GET CONFUSIONS
    # ============================================================

    def _get_confusions(self, profile):

        confusions = {}

        mastery = profile.get(
            "alphabet_mastery",
            {}
        )

        for alphabet, data in mastery.items():

            if not isinstance(data, dict):

                continue

            confusion_data = data.get(
                "confused_with",
                {}
            )

            if confusion_data:

                confusions[alphabet] = (
                    confusion_data
                )

        return confusions

    # ========================================================
    # START PRACTICE
    # ========================================================

    def start_practice(
        self,
        db,
        lesson_id: int,
        student_id: str = "default_student",
    ):

        lesson = (
            self.lesson_service.get_lesson_by_id(
                db,
                lesson_id
            )
        )

        if lesson is None:

            return {
                "success": False,
                "message": "Lesson not found.",
            }

        profile = (
            self.learner_profile_service.get_profile(
                student_id
            )
        )

        current_letter = profile.get(
            "current_letter",
            "A"
        )

        next_letter = profile.get(
            "next_letter",
            current_letter
        )

        completed_letters = profile.get(
            "completed_letters",
            []
        )

        session = (
            self.session_service.start_session(
                lesson_id=lesson_id,
                student_id=student_id,
            )
        )

        session_id = session["session_id"]

        session["current_letter"] = (
            current_letter
        )

        session["next_letter"] = (
            next_letter
        )

        session["completed_letters"] = (
            completed_letters.copy()
        )

        session["remaining_letters"] = [

            letter

            for letter in
            self.session_service.alphabets

            if letter not in completed_letters

        ]

        self.learner_profile_service.increment_sessions(
            student_id
        )

        self.temporal_buffers[
            session_id
        ] = TemporalBuffer(
            max_frames=30
        )

        self.stable_detectors[
            session_id
        ] = StableGestureDetector(
            required_stable_frames=3,
            confidence_threshold=0.10,
            stability_threshold=60,
            history_size=5,
        )

        self.stability_calculators[
            session_id
        ] = StabilityCalculator()

        self.motion_metrics[
            session_id
        ] = MotionMetrics()

        self.performance_monitors[
            session_id
        ] = PerformanceMonitor()

        session["latest_prediction"] = None

        session["latest_confidence"] = 0.0

        session["latest_stable_prediction"] = {

            "stable": False,

            "prediction": None,

            "confidence": 0.0,

            "stable_frames": 0,

            "unstable_frames": 0,

            "required_frames": 3,

            "gesture_stability": 0.0,

            "majority_prediction": None,

            "majority_ratio": 0.0,

            "last_stable_prediction": None,

            "new_stable": False,
        }

        self.session_service.update_session(
            session_id,
            session
        )

        lesson_response = {

            "id": lesson.id,

            "title": lesson.title,

            "description": lesson.description,

            "category": lesson.category,

            "sign": lesson.sign,

            "image_url": lesson.image_url,

            "video_url": lesson.video_url,

            "is_active": lesson.is_active,
        }

        return {

            "success": True,

            "message":
                "Practice session started.",

            "session":
                session,

            "lesson":
                lesson_response,

            "expected_letter":
                current_letter,
        }

    # ========================================================
    # PROCESS FRAME
    # ========================================================

    def process_frame(
        self,
        session_id,
        landmarks,
        hand_count=1,
        person_count=1,
        body_visible=True,
    ):

        session = (
            self.session_service.get_session(
                session_id
            )
        )

        if session is None:

            return {

                "success": False,

                "message":
                    "Session not found.",

                "prediction":
                    "UNKNOWN",

                "confidence":
                    0.0,
            }

        temporal_buffer = (
            self.temporal_buffers.get(
                session_id
            )
        )

        detector = (
            self.stable_detectors.get(
                session_id
            )
        )

        stability = (
            self.stability_calculators.get(
                session_id
            )
        )

        motion = (
            self.motion_metrics.get(
                session_id
            )
        )

        monitor = (
            self.performance_monitors.get(
                session_id
            )
        )

        if monitor:

            monitor.update_frame()

        try:

            frame_result = (
                self.frame_detection_service.detect(
                    landmarks=landmarks,
                    hand_count=hand_count,
                    person_count=person_count,
                    body_visible=body_visible,
                )
            )

        except Exception as e:

            return {

                "success": False,

                "message":
                    "Frame detection failed.",

                "prediction":
                    "UNKNOWN",

                "confidence":
                    0.0,

                "error":
                    str(e),
            }

        validation = frame_result.get(
            "validation",
            {
                "valid": False,
                "reason":
                    "Validation result missing.",
            },
        )

        if not validation.get(
            "valid",
            False
        ):

            invalid_stable_prediction = {

                "stable": False,

                "prediction": None,

                "confidence": 0.0,

                "stable_frames": 0,

                "unstable_frames": 0,

                "required_frames": (
                    detector.required_stable_frames
                    if detector
                    else 3
                ),

                "gesture_stability": 0.0,

                "majority_prediction": None,

                "majority_ratio": 0.0,

                "last_stable_prediction": (
                    detector.last_stable_prediction
                    if detector
                    else None
                ),

                "new_stable": False,
            }

            performance = (
                monitor.get_metrics()
                if monitor
                else {}
            )

            return {

                "success": False,

                "validation":
                    validation,

                "prediction":
                    "UNKNOWN",

                "confidence":
                    0.0,

                "top_predictions":
                    [],

                "stable_prediction":
                    invalid_stable_prediction,

                "stable":
                    False,

                "stable_gesture":
                    None,

                "stable_confidence":
                    0.0,

                "stable_frames":
                    0,

                "required_frames": (
                    detector.required_stable_frames
                    if detector
                    else 3
                ),

                "gesture_stability":
                    0.0,

                "new_stable":
                    False,

                "buffer_size": (
                    temporal_buffer.size()
                    if temporal_buffer
                    else 0
                ),

                "buffer_full": (
                    temporal_buffer.is_full()
                    if temporal_buffer
                    else False
                ),

                "motion_metrics":
                    {},

                "performance":
                    performance,
            }

        if temporal_buffer:

            try:

                temporal_buffer.add_frame(
                    landmarks
                )

            except Exception:

                pass

        if motion:

            try:

                motion.add_landmarks(
                    landmarks
                )

            except Exception:

                pass

        prediction = "UNKNOWN"

        confidence = 0.0

        latency = 0.0

        top_predictions = []

        stable_prediction = {

            "stable": False,

            "prediction": None,

            "confidence": 0.0,

            "stable_frames": 0,

            "unstable_frames": 0,

            "required_frames": (
                detector.required_stable_frames
                if detector
                else 3
            ),

            "gesture_stability": 0.0,

            "majority_prediction": None,

            "majority_ratio": 0.0,

            "last_stable_prediction": (
                detector.last_stable_prediction
                if detector
                else None
            ),

            "new_stable": False,
        }

        try:

            prediction_result = (
                self.gesture_service.predict(
                    landmarks
                )
            )

            if prediction_result:

                prediction = (
                    self.clean_prediction(
                        prediction_result.get(
                            "prediction",
                            "UNKNOWN"
                        )
                    )
                )

                confidence = (
                    self.normalize_confidence(
                        prediction_result.get(
                            "confidence",
                            0
                        )
                    )
                )

                latency = (
                    prediction_result.get(
                        "processing_time",
                        0
                    )
                )

                top_predictions = (
                    prediction_result.get(
                        "top_predictions",
                        []
                    )
                )

        except Exception:

            pass

        if monitor:

            try:

                monitor.update_latency(
                    latency
                )

                monitor.update_confidence(
                    confidence
                )

            except Exception:

                pass

        if motion:

            try:

                motion.add_confidence(
                    confidence
                )

            except Exception:

                pass

        session["latest_prediction"] = (
            prediction
        )

        session["latest_confidence"] = (
            confidence
        )

        if detector is not None:

            try:

                stable_prediction = (
                    detector.update(
                        prediction=prediction,
                        confidence=confidence
                    )
                )

            except Exception:

                pass

            if not isinstance(
                stable_prediction,
                dict
            ):

                stable_prediction = {

                    "stable": False,

                    "prediction": None,

                    "confidence": 0.0,

                    "stable_frames": 0,

                    "unstable_frames": 0,

                    "required_frames":
                        detector.required_stable_frames,

                    "gesture_stability": 0.0,

                    "majority_prediction":
                        None,

                    "majority_ratio":
                        0.0,

                    "last_stable_prediction":
                        detector.last_stable_prediction,

                    "new_stable":
                        False,
                }

        if stable_prediction.get(
            "stable",
            False
        ):

            stable_gesture = (
                self.clean_prediction(
                    stable_prediction.get(
                        "prediction",
                        prediction
                    )
                )
            )

            stable_confidence = (
                self.normalize_confidence(
                    stable_prediction.get(
                        "confidence",
                        confidence
                    )
                )
            )

            session["latest_prediction"] = (
                stable_gesture
            )

            session["latest_confidence"] = (
                stable_confidence
            )

        session["latest_stable_prediction"] = (
            stable_prediction
        )

        if stability:

            try:

                stability.update(
                    prediction=prediction,
                    confidence=confidence,
                    stable=stable_prediction.get(
                        "stable",
                        False
                    ),
                )

            except Exception:

                pass

        motion_metrics = {}

        if motion:

            try:

                motion_metrics.update(
                    motion.get_metrics()
                )

            except Exception:

                pass

        if stability:

            try:

                motion_metrics.update(
                    stability.get_metrics()
                )

            except Exception:

                pass

        performance = (
            monitor.get_metrics()
            if monitor
            else {}
        )

        buffer_size = (
            temporal_buffer.size()
            if temporal_buffer
            else 0
        )

        buffer_full = (
            temporal_buffer.is_full()
            if temporal_buffer
            else False
        )

        self.session_service.update_session(
            session_id,
            session
        )

        return {

            "success": True,

            "validation":
                validation,

            "prediction":
                prediction,

            "confidence":
                round(
                    confidence,
                    3
                ),

            "top_predictions":
                top_predictions,

            "stable_prediction":
                stable_prediction,

            "stable":
                stable_prediction.get(
                    "stable",
                    False
                ),

            "stable_gesture":
                stable_prediction.get(
                    "prediction"
                ),

            "stable_confidence":
                self.normalize_confidence(
                    stable_prediction.get(
                        "confidence",
                        0
                    )
                ),

            "stable_frames":
                stable_prediction.get(
                    "stable_frames",
                    0
                ),

            "required_frames":
                stable_prediction.get(
                    "required_frames",
                    detector.required_stable_frames
                    if detector
                    else 3
                ),

            "gesture_stability":
                stable_prediction.get(
                    "gesture_stability",
                    0
                ),

            "new_stable":
                stable_prediction.get(
                    "new_stable",
                    False
                ),

            "buffer_size":
                buffer_size,

            "buffer_full":
                buffer_full,

            "motion_metrics":
                motion_metrics,

            "performance":
                performance,
        }

    # ==================================================
    # RECORD FINAL ATTEMPT
    # ==================================================

    def record_attempt(
        self,
        db,
        session_id,
        landmarks,
        stable_prediction=None,
        motion_metrics=None,
    ):

        # ==================================================
        # 1. GET SESSION
        # ==================================================

        session = (
            self.session_service.get_session(
                session_id
            )
        )

        if session is None:

            return {

                "success": False,

                "message":
                    "Session not found.",
            }

        student_id = session.get(
            "student_id",
            "default_student"
        )

        # ==================================================
        # 2. EXPECTED LETTER
        # ==================================================

        expected = self.clean_prediction(
            session.get(
                "current_letter",
                session.get(
                    "selected_letter",
                    "A"
                )
            )
        )

        if expected == "COMPLETED":

            return {

                "success": False,

                "message":
                    "Learner has already completed all letters.",

                "completed":
                    True,
            }

        # ==================================================
        # 3. STORED PREDICTION
        # ==================================================

        stored_prediction = (
            self.clean_prediction(
                session.get(
                    "latest_prediction",
                    "UNKNOWN"
                )
            )
        )

        stored_confidence = (
            self.normalize_confidence(
                session.get(
                    "latest_confidence",
                    0
                )
            )
        )

        stored_stable = (
            session.get(
                "latest_stable_prediction",
                {}
            )
        )

        final_prediction = (
            stored_prediction
        )

        final_confidence = (
            stored_confidence
        )

        if (

            stored_stable

            and

            stored_stable.get(
                "stable"
            )

            and

            stored_stable.get(
                "prediction"
            )

        ):

            final_prediction = (
                self.clean_prediction(
                    stored_stable.get(
                        "prediction"
                    )
                )
            )

            final_confidence = (
                self.normalize_confidence(
                    stored_stable.get(
                        "confidence",
                        stored_confidence
                    )
                )
            )

        if stable_prediction is None:

            stable_prediction = (
                stored_stable
            )

        if (

            stable_prediction

            and

            stable_prediction.get(
                "stable",
                False
            )

            and

            stable_prediction.get(
                "prediction"
            )

        ):

            final_prediction = (
                self.clean_prediction(
                    stable_prediction.get(
                        "prediction"
                    )
                )
            )

            final_confidence = (
                self.normalize_confidence(
                    stable_prediction.get(
                        "confidence",
                        stored_confidence
                    )
                )
            )

        elif (

            final_prediction
            in (
                None,
                "",
                "UNKNOWN"
            )

            and

            landmarks

            and

            len(landmarks) == 21

        ):

            try:

                prediction_result = (
                    self.gesture_service.predict(
                        landmarks
                    )
                )

                if prediction_result:

                    final_prediction = (
                        self.clean_prediction(
                            prediction_result.get(
                                "prediction",
                                "UNKNOWN"
                            )
                        )
                    )

                    final_confidence = (
                        self.normalize_confidence(
                            prediction_result.get(
                                "confidence",
                                0
                            )
                        )
                    )

            except Exception:

                final_prediction = "UNKNOWN"

                final_confidence = 0.0

        final_prediction = (
            self.clean_prediction(
                final_prediction
            )
        )

        final_confidence = (
            self.normalize_confidence(
                final_confidence
            )
        )

        # ==================================================
        # 4. CORRECT / INCORRECT
        # ==================================================

        correct = (
            expected == final_prediction
        )

        # ==================================================
        # 5. VALIDATE LANDMARKS
        # ==================================================

        if (

            landmarks

            and

            len(landmarks) == 21

        ):

            validation = (
                self.frame_validator.validate(
                    landmarks=landmarks,
                    hand_count=1,
                    person_count=1,
                    body_visible=True,
                )
            )

        else:

            validation = {

                "valid": True,

                "reason":
                    "USING_STORED_PREDICTION",
            }

        # ==================================================
        # MOTION
        # ==================================================

        final_motion = {}

        if motion_metrics:

            final_motion.update(
                motion_metrics
            )

        runtime_motion = (
            self.motion_metrics.get(
                session_id
            )
        )

        if runtime_motion:

            final_motion.update(
                runtime_motion.get_metrics()
            )

        stability_calculator = (
            self.stability_calculators.get(
                session_id
            )
        )

        if stability_calculator:

            final_motion.update(
                stability_calculator.get_metrics()
            )

        # ==================================================
        # 6. FEEDBACK
        # ==================================================

        assessment_id = (
            str(
                uuid.uuid4()
            )[:8].upper()
        )

        try:

            feedback = (
                self.feedback_engine.evaluate(

                    expected=expected,

                    predicted=final_prediction,

                    confidence=final_confidence,

                    landmarks=landmarks,

                    validation_reason=
                        validation.get(
                            "reason"
                        ),

                    stable_prediction=
                        stable_prediction,

                    motion_metrics=
                        final_motion,
                )
            )

        except Exception as e:

            feedback = {

                "message":
                    "Unable to generate detailed feedback.",

                "error":
                    str(e),
            }

        # ==================================================
        # 7. SIGN SCORE
        # ==================================================

        try:

            sign_score = (
                self.score_calculator.calculate(

                    correct=correct,

                    confidence=(
                        final_confidence * 100
                    ),

                    stability=
                        final_motion.get(
                            "gesture_stability",
                            0
                        ),

                    time_taken=
                        final_motion.get(
                            "time_taken",
                            0
                        ),
                )
            )

        except Exception:

            sign_score = {

                "overall_score":
                    0,

                "grade":
                    "Needs Improvement",

                "components":
                    {},
            }

        # ==================================================
        # 8. ATTEMPT DATA
        # ==================================================

        attempt_data = {

            "assessment_id":
                assessment_id,

            "student_id":
                student_id,

            "session_id":
                session_id,

            "expected":
                expected,

            "predicted":
                final_prediction,

            "confidence":
                final_confidence,

            "correct":
                correct,

            "motion_metrics":
                final_motion,

            "feedback":
                feedback,

            "sign_score":
                sign_score,

            "timestamp":
                datetime.now().isoformat(),
        }

        # ==================================================
        # 9. RECORD THROUGH SESSION SERVICE
        # ==================================================

        updated_session = (
            self.session_service.record_attempt(
                session_id,
                attempt_data
            )
        )
        profile = (
    self.learner_profile_service.update_after_attempt(
        student_id=student_id,
        alphabet=expected,
        predicted=final_prediction,
        confidence=final_confidence,
        correct=correct,
    )
)

        if updated_session is None:

            return {

                "success": False,

                "message":
                    "Unable to record practice attempt.",
            }

        session = updated_session

        # ==================================================
        # 10. ADD ATTEMPT TO HISTORY
        # ==================================================

        

        # ==================================================
        # 11. UPDATED PROFILE
        # ==================================================

        

        session["completed_letters"] = (
            profile.get(
                "completed_letters",
                []
            ).copy()
        )

        session["current_letter"] = (
            profile.get(
                "current_letter",
                expected
            )
        )

        session["next_letter"] = (
            profile.get(
                "next_letter"
            )
        )

        attempt_data["completed_letters"] = (
            session["completed_letters"]
        )

        attempt_data["current_letter"] = (
            session["current_letter"]
        )

        attempt_data["next_letter"] = (
            session["next_letter"]
        )
        self.assessment_history.add_attempt(
                    attempt_data
                )

        # ==================================================
        # 12. LEARNING STATE
        # ==================================================

        history = (
            self.assessment_history.get_student_history(
                student_id
            )
        )

        try:

            learning_state = (
                self.learning_state.calculate(
                    history
                )
            )

        except Exception:

            learning_state = {}

        # ==================================================
        # 13. ERROR ANALYSIS
        # ==================================================

        try:

            analysis = (
                self.error_analysis_service.analyze_student(
                    student_id
                )
            )

        except Exception:

            analysis = {}

        performance_trends = (
            analysis.get(
                "performance_trends",
                []
            )
        )

        try:

            confusion_pairs = (
                self._get_confusions(
                    profile
                )
            )

        except Exception:

            confusion_pairs = {}

        # ==================================================
        # 14. RECOMMENDATIONS
        # ==================================================

        try:

            recommendations = (
                self.recommendation_engine.generate(

                    learner_profile=
                        profile,

                    confusion_pairs=
                        confusion_pairs,

                    trends=
                        performance_trends,
                )
            )

        except Exception:

            recommendations = []

        if not recommendations:

            next_letter = profile.get(
                "next_letter"
            )

            if (

                next_letter

                and

                next_letter != "COMPLETED"

            ):

                recommendations.append({

                    "alphabet":
                        next_letter,

                    "reason":
                        "Continue sequential learning.",

                    "priority":
                        "HIGH",
                })

        # ==================================================
        # 15. PRACTICE QUEUE
        # ==================================================

        try:

            self.practice_queue.update_queue(
                student_id,
                recommendations
            )

        except Exception:

            pass

        try:

            next_practice = (
                self.practice_queue.get_next_practice(
                    student_id
                )
            )

        except Exception:

            next_practice = None

        recommended_letter = (

            next_practice.get(
                "alphabet"
            )

            if next_practice

            else None

        )

        # ==================================================
        # 16. REMAINING LETTERS
        # ==================================================

        completed_letters = set(
            session.get(
                "completed_letters",
                []
            )
        )

        session["remaining_letters"] = [

            letter

            for letter in
            self.session_service.alphabets

            if letter not in completed_letters

        ]

        self.session_service.update_session(
            session_id,
            session
        )

        # ==================================================
        # 17. GET CURRENT LETTER ACCURACY
        # ==================================================
        #
        # IMPORTANT:
        #
        # This is the accuracy for the letter that was
        # actually assessed.
        #
        # Example:
        #
        # A: wrong  -> 0%
        # A: correct -> 50%
        # A: correct -> 66.67%
        #
        # It is NOT simply 100% when the latest attempt
        # is correct.
        #
        # ==================================================

        letter_accuracy = (
    profile
    .get(
        "alphabet_mastery",
        {}
    )
    .get(
        expected,
        {}
    )
    .get(
        "accuracy",
        0
    )
)

        try:

            letter_accuracy = float(
                letter_accuracy
            )

        except (
            TypeError,
            ValueError
        ):

            letter_accuracy = 0.0

        letter_accuracy = max(
            0.0,
            min(
                100.0,
                letter_accuracy
            )
        )

        # ==================================================
        # 18. DASHBOARD
        # ==================================================

        try:

            dashboard = (
                self.dashboard_service.get_dashboard(
                    student_id
                )
            )

        except Exception:

            dashboard = {}

        # ==================================================
        # 19. FINAL RESPONSE
        # ==================================================

        return {

            "success":
                True,

            "assessment": {

                "assessment_id":
                    assessment_id,

                "expected":
                    expected,

                "predicted":
                    final_prediction,

                "confidence":
                    round(
                        final_confidence,
                        3
                    ),

                "correct":
                    correct,

                # ==========================================
                # IMPORTANT FIX
                # ==========================================

                "accuracy":
                    round(
                        letter_accuracy,
                        2
                    ),
            },

            "feedback":
                feedback,

            "sign_score":
                sign_score,

            "session":
                session,

            "profile":
                profile,

            "learning_state":
                learning_state,

            "recommendations":
                recommendations,

            "next_practice": {

                "alphabet":
                    recommended_letter,

                "details":
                    next_practice,
            },

            "dashboard":
                dashboard,
        }

    # ==================================================
    # DASHBOARD & PROFILE DATA ACCESSORS
    # ==================================================

    def get_dashboard(
        self,
        student_id: str
    ):

        return (
            self.dashboard_service.get_dashboard(
                student_id
            )
        )

    def get_learner_profile(
        self,
        student_id: str
    ):

        return (
            self.learner_profile_service.get_profile(
                student_id
            )
        )

    def get_student_assessments(
        self,
        student_id: str
    ):

        return (
            self.assessment_history.get_student_history(
                student_id
            )
        )

    def get_session_assessments(
        self,
        session_id: str
    ):

        return (
            self.assessment_history.get_session_history(
                session_id
            )
        )

    def get_assessment_history(self):

        return (
            self.assessment_history.get_all()
        )

    def get_error_analysis(
        self,
        student_id: str
    ):

        return (
            self.error_analysis_service.analyze_student(
                student_id
            )
        )

    def get_student_report(
        self,
        student_id: str
    ):

        return (
            self.report_service.get_student_report(
                student_id
            )
        )