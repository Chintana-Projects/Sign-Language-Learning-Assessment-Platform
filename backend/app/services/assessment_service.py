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


# ============================================================
# ASSESSMENT SERVICE
# ============================================================

class AssessmentService:

    """
    ============================================================
    Assessment Service
    ============================================================

    Responsibilities:

    • Practice Session Management
    • Frame Processing
    • Gesture Prediction
    • Temporal Stability
    • Motion Metrics
    • Performance Monitoring
    • Gesture Assessment
    • Feedback Generation
    • Sign Scoring
    • Learner Profile Updates
    • Error Analysis
    • Recommendations
    • Practice Queue
    • Dashboard Analytics
    • Assessment History
    ============================================================
    """

    def __init__(self):

        print("LIVE PRACTICE CREATED")
        print("AssessmentService ID:", id(self))

        # =====================================================
        # CORE SERVICES
        # =====================================================

        self.lesson_service = LessonService()

        self.session_service = SessionService()

        self.gesture_service = GestureService()

        self.frame_detection_service = FrameDetectionService()


        # =====================================================
        # FEEDBACK
        # =====================================================

        self.feedback_engine = FeedbackEngine()

        self.personalized_feedback = PersonalizedFeedback()

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
        # LEARNING STATE
        # =====================================================

        self.learning_state = LearningState()


        # =====================================================
        # ERROR ANALYSIS
        # =====================================================

        self.error_analysis_service = (
            ErrorAnalysisService(
                self.assessment_history
            )
        )


        # =====================================================
        # DASHBOARD
        # =====================================================

        self.dashboard_service = DashboardService(
            learner_profile_service=(
                self.learner_profile_service
            ),
            recommendation_engine=(
                self.recommendation_engine
            ),
            assessment_history=(
                self.assessment_history
            ),
            learning_state=(
                self.learning_state
            ),
        )


        # =====================================================
        # FRAME VALIDATION
        # =====================================================

        self.frame_validator = FrameValidator()


        # =====================================================
        # PRACTICE QUEUE
        # =====================================================

        self.practice_queue = PracticeQueue()


        # =====================================================
        # STUDENT ATTEMPT TRACKERS
        # =====================================================

        self.student_trackers = {}


        # =====================================================
        # SESSION-SPECIFIC RUNTIME COMPONENTS
        # =====================================================
        #
        # IMPORTANT:
        #
        # Every practice session gets its own:
        #
        # • TemporalBuffer
        # • StableGestureDetector
        # • StabilityCalculator
        # • MotionMetrics
        # • PerformanceMonitor
        #
        # Do NOT make these global.
        #
        # This preserves the working session architecture.
        # =====================================================

        self.temporal_buffers = {}

        self.stable_detectors = {}

        self.stability_calculators = {}

        self.motion_metrics = {}

        self.performance_monitors = {}
            # ========================================================
    # STUDENT TRACKER
    # ========================================================

    def get_tracker(self, student_id):

        if student_id not in self.student_trackers:

            self.student_trackers[student_id] = (
                AttemptTracker(student_id)
            )

        return self.student_trackers[student_id]


    # ========================================================
    # HELPER: CLEAN PREDICTION
    # ========================================================

    def clean_prediction(self, prediction):

        if prediction is None:
            return "UNKNOWN"

        return str(prediction).strip().upper()


    # ========================================================
    # HELPER: NORMALIZE CONFIDENCE
    # ========================================================

    def normalize_confidence(self, confidence):

        try:
            confidence = float(confidence)

        except (TypeError, ValueError):
            return 0.0

        # Some models/services may return:
        #
        # 0.985
        #
        # while others may return:
        #
        # 98.5
        #
        # Normalize both to 0-1.

        if confidence > 1:
            confidence /= 100.0

        confidence = max(
            0.0,
            min(1.0, confidence)
        )

        return round(confidence, 4)


    # ========================================================
    # HELPER: CONFUSION DATA
    # ========================================================

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
        """
        Start a new practice session.

        Flow:

        1. Validate lesson
        2. Load learner profile
        3. Create session
        4. Synchronize learner progress
        5. Create session-specific runtime components
        6. Store runtime state
        7. Return lesson information
        """

        # ====================================================
        # 1. VALIDATE LESSON
        # ====================================================

        lesson = self.lesson_service.get_lesson_by_id(
    db,
    lesson_id
)

        if lesson is None:

            return {
                "success": False,
                "message": "Lesson not found.",
            }


        # ====================================================
        # 2. LOAD LEARNER PROFILE
        # ====================================================

        profile = self.learner_profile_service.get_profile(
            student_id
        )

        current_letter = profile.get(
            "current_letter",
            "A",
        )

        next_letter = profile.get(
            "next_letter",
            current_letter,
        )

        completed_letters = profile.get(
            "completed_letters",
            [],
        )


        # ====================================================
        # DEBUG
        # ====================================================

        print(
            "\n========== START PRACTICE =========="
        )

        print(
            "AssessmentService ID :",
            id(self),
        )

        print(
            "SessionService ID    :",
            id(self.session_service),
        )

        print(
            "Current Letter       :",
            current_letter,
        )


        # ====================================================
        # 3. CREATE SESSION
        # ====================================================

        session = self.session_service.start_session(
            lesson_id=lesson_id,
            student_id=student_id,
        )

        session_id = session["session_id"]


        # ====================================================
        # 4. SYNCHRONIZE SESSION WITH PROFILE
        # ====================================================

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

            for letter in self.session_service.alphabets

            if letter not in completed_letters
        ]


        # ====================================================
        # 5. INCREMENT SESSION COUNT
        # ====================================================

        self.learner_profile_service.increment_sessions(
            student_id
        )


        # ====================================================
        # 6. CREATE SESSION-SPECIFIC TEMPORAL BUFFER
        # ====================================================

        self.temporal_buffers[session_id] = (
            TemporalBuffer(
                max_frames=30
            )
        )


        # ====================================================
        # 7. CREATE SESSION-SPECIFIC STABLE DETECTOR
        # ====================================================
        #
        # IMPORTANT:
        #
        # This detector belongs ONLY to this session.
        #
        # Therefore:
        #
        # self.stable_detectors[session_id]
        #
        # must be used later inside process_frame().
        #
        # This is the part we do NOT want to replace
        # with a global detector.
        # ====================================================

        self.stable_detectors[session_id] = (
            StableGestureDetector(
                required_stable_frames=3,
                confidence_threshold=0.10,
                stability_threshold=60,
                history_size=5,
            )
        )


        # ====================================================
        # 8. STABILITY CALCULATOR
        # ====================================================

        self.stability_calculators[session_id] = (
            StabilityCalculator()
        )


        # ====================================================
        # 9. MOTION METRICS
        # ====================================================

        self.motion_metrics[session_id] = (
            MotionMetrics()
        )


        # ====================================================
        # 10. PERFORMANCE MONITOR
        # ====================================================

        self.performance_monitors[session_id] = (
            PerformanceMonitor()
        )


        # ====================================================
        # 11. INITIAL RUNTIME PREDICTION STATE
        # ====================================================

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


        # ====================================================
        # 12. SAVE SESSION
        # ====================================================

        self.session_service.update_session(
            session_id,
            session,
        )


        # ====================================================
        # DEBUG
        # ====================================================

        print(
            "Session Created :",
            session_id,
        )

        print(
            "Current Letter  :",
            session["current_letter"],
        )

        print(
            "Next Letter     :",
            session["next_letter"],
        )

        print(
            "Completed       :",
            session["completed_letters"],
        )

        print(
            "Detector ID     :",
            id(
                self.stable_detectors[
                    session_id
                ]
            ),
        )


        # ====================================================
        # 13. BUILD LESSON RESPONSE
        # ====================================================

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

        print(
            "\n========== START DEBUG =========="
        )

        print(
            "lesson_id       :",
            lesson_id,
        )

        print(
            "profile current :",
            current_letter,
        )

        print(
            "lesson sign     :",
            lesson_response.get(
                "sign"
            ),
        )

        print(
    "lesson image    :",
    lesson_response.get(
        "image_url"
    ),
)

        print(
            "================================="
        )


        # ====================================================
        # 14. RETURN
        # ====================================================

        return {

            "success": True,

            "message": (
                "Practice session started."
            ),

            "session": session,

            "lesson": lesson_response,

            "expected_letter": current_letter,
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
        """
        Process exactly ONE webcam frame.

        Flow:

        1. Get session
        2. Get session-specific runtime components
        3. Validate frame
        4. Store landmarks
        5. Predict gesture ONCE
        6. Update stable detector ONCE
        7. Update motion/stability/performance metrics
        8. Save latest runtime state
        9. Return complete frame result
        """

        print("\n" + "=" * 60)
        print("FRAME RECEIVED")
        print("=" * 60)

        print(
            "AssessmentService ID:",
            id(self),
        )

        print(
            "Detector Dictionary ID:",
            id(self.stable_detectors),
        )

        print(
            "SESSION:",
            session_id,
        )


        # ====================================================
        # 1. GET SESSION
        # ====================================================

        session = self.session_service.get_session(
            session_id
        )

        if session is None:

            print(
                "ERROR: Session not found:",
                session_id,
            )

            return {
                "success": False,
                "message": "Session not found.",
                "prediction": "UNKNOWN",
                "confidence": 0.0,
            }


        # ====================================================
        # 2. GET SESSION-SPECIFIC RUNTIME COMPONENTS
        # ====================================================

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


        # ====================================================
        # 3. DEBUG RUNTIME COMPONENTS
        # ====================================================

        print(
            "\n========== RUNTIME DEBUG =========="
        )

        print(
            "Session ID:",
            session_id,
        )

        print(
            "Temporal Buffer:",
            temporal_buffer,
        )

        print(
            "Stable Detector:",
            detector,
        )

        print(
    "Stable Detector ID:",
    id(detector)
    if detector is not None
    else None,
)
        print(
            "Stability Calculator:",
            stability,
        )

        print(
            "Motion Metrics:",
            motion,
        )

        print(
            "Performance Monitor:",
            monitor,
        )

        print(
            "Available Detector Sessions:",
            list(
                self.stable_detectors.keys()
            ),
        )

        print(
            "===================================="
        )


        # ====================================================
        # 4. PERFORMANCE MONITOR — FRAME RECEIVED
        # ====================================================

        if monitor:

            monitor.update_frame()


        print(
            "\n========== FRAME INPUT =========="
        )

        print(
            "Hand Count:",
            hand_count,
        )

        print(
            "Person Count:",
            person_count,
        )

        print(
            "Body Visible:",
            body_visible,
        )


        # ====================================================
        # 5. FRAME DETECTION / VALIDATION
        # ====================================================

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

            print(
                "Frame Detection Error:",
                e,
            )

            return {
                "success": False,
                "message": (
                    "Frame detection failed."
                ),
                "prediction": "UNKNOWN",
                "confidence": 0.0,
                "error": str(e),
            }


        validation = frame_result.get(
            "validation",
            {
                "valid": False,
                "reason": (
                    "Validation result missing."
                ),
            },
        )


        # ====================================================
        # 6. DEBUG FRAME DETECTION
        # ====================================================

        print(
            "\n========== FRAME DETECTION =========="
        )

        print(
            "Hand Count:",
            hand_count,
        )

        print(
            "Person Count:",
            person_count,
        )

        print(
            "Body Visible:",
            body_visible,
        )

        print(
            "Landmarks:",
            len(landmarks)
            if landmarks
            else 0,
        )


        # ====================================================
        # 7. INVALID FRAME
        # ====================================================

        if not validation.get(
            "valid",
            False,
        ):

            print(
                "Frame Rejected"
            )

            print(
                "Validation:",
                validation,
            )


            # ---------------------------------------------
            # Do NOT call GestureService.predict()
            # for an invalid frame.
            # ---------------------------------------------

            invalid_stable_prediction = {

                "stable": False,

                "prediction": None,

                "confidence": 0.0,

                "stable_frames": 0,

                "unstable_frames": 0,

                "required_frames": (
    detector.required_stable_frames
    if detector is not None
    else 3
),

                "gesture_stability": 0.0,

                "majority_prediction": None,

                "majority_ratio": 0.0,

                "last_stable_prediction": (
    detector.last_stable_prediction
    if detector is not None
    else None
),

                "new_stable": False,
            }


            if monitor:

                performance = (
                    monitor.get_metrics()
                )

            else:

                performance = {}


            return {

                "success": False,

                "validation": validation,

                "prediction": "UNKNOWN",

                "confidence": 0.0,

                "top_predictions": [],

                "stable_prediction": (
                    invalid_stable_prediction
                ),

                "stable": False,

                "stable_gesture": None,

                "stable_confidence": 0.0,

                "stable_frames": 0,

                "required_frames": (
    detector.required_stable_frames
    if detector is not None
    else 3
),
                "gesture_stability": 0.0,

                "new_stable": False,

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

                "motion_metrics": {},

                "performance": performance,
            }


        # ====================================================
        # 8. VALID FRAME
        # ====================================================

        print(
            "Frame Accepted"
        )

        print(
            "Visible Landmarks:",
            frame_result.get(
                "visible_landmarks",
                len(landmarks)
                if landmarks
                else 0,
            ),
        )

        print(
            "Hand Width:",
            frame_result.get(
                "hand_width",
                0,
            ),
        )

        print(
            "Hand Height:",
            frame_result.get(
                "hand_height",
                0,
            ),
        )

        print(
            "Warnings:",
            frame_result.get(
                "warnings",
                [],
            ),
        )

        print(
            "===================================="
        )


        # ====================================================
        # 9. STORE LANDMARK FRAME
        # ====================================================

        if temporal_buffer:

            try:

                temporal_buffer.add_frame(
                    landmarks
                )

            except Exception as e:

                print(
                    "Temporal Buffer Error:",
                    e,
                )


        # ====================================================
        # 10. UPDATE MOTION METRICS
        # ====================================================

        if motion:

            try:

                motion.add_landmarks(
                    landmarks
                )

            except Exception as e:

                print(
                    "Motion Landmark Error:",
                    e,
                )


        # ====================================================
        # 11. INITIAL PREDICTION STATE
        # ====================================================

        prediction = "UNKNOWN"

        confidence = 0.0

        latency = 0.0

        top_predictions = []


        # ====================================================
        # 12. INITIAL STABLE PREDICTION STATE
        # ====================================================

        stable_prediction = {

            "stable": False,

            "prediction": None,

            "confidence": 0.0,

            "stable_frames": 0,

            "unstable_frames": 0,

            "required_frames": (
    detector.required_stable_frames
    if detector is not None
    else 3
),

            "gesture_stability": 0.0,

            "majority_prediction": None,

            "majority_ratio": 0.0,

            "last_stable_prediction": (
    detector.last_stable_prediction
    if detector is not None
    else None
),

            "new_stable": False,
        }


        # ====================================================
        # 13. GESTURE PREDICTION
        # ====================================================
        #
        # IMPORTANT:
        #
        # GestureService.predict() is called EXACTLY ONCE
        # for this valid frame.
        #
        # Do not call it again later in this method.
        # ====================================================

        prediction_result = None

        try:

            prediction_result = (
                self.gesture_service.predict(
                    landmarks
                )
            )

        except Exception as e:

            print(
                "Prediction Error:",
                e,
            )


        # ====================================================
        # 14. PROCESS PREDICTION RESULT
        # ====================================================

        if prediction_result:

            prediction = self.clean_prediction(
                prediction_result.get(
                    "prediction",
                    "UNKNOWN",
                )
            )

            confidence = (
                self.normalize_confidence(
                    prediction_result.get(
                        "confidence",
                        0,
                    )
                )
            )

            latency = prediction_result.get(
                "processing_time",
                0,
            )

            top_predictions = (
                prediction_result.get(
                    "top_predictions",
                    [],
                )
            )


        # ====================================================
        # 15. PREDICTION DEBUG
        # ====================================================

        print(
            "\n========== GESTURE PREDICTION =========="
        )

        print(
            "Prediction:",
            prediction,
        )

        print(
            "Confidence:",
            confidence,
        )

        print(
            "Latency:",
            latency,
        )

        print(
            "Top Predictions:",
            top_predictions,
        )

        print(
            "========================================"
        )


        # ====================================================
        # 16. PERFORMANCE MONITOR
        # ====================================================

        if monitor:

            try:

                monitor.update_latency(
                    latency
                )

                monitor.update_confidence(
                    confidence
                )

            except Exception as e:

                print(
                    "Performance Update Error:",
                    e,
                )


        # ====================================================
        # 17. MOTION CONFIDENCE
        # ====================================================

        if motion:

            try:

                motion.add_confidence(
                    confidence
                )

            except Exception as e:

                print(
                    "Motion Confidence Error:",
                    e,
                )


        # ====================================================
        # 18. SAVE RAW LATEST PREDICTION
        # ====================================================

        session["latest_prediction"] = (
            prediction
        )

        session["latest_confidence"] = (
            confidence
        )


        # ====================================================
        # 19. STABLE GESTURE DETECTOR
        # ====================================================

        if detector is not None:
            print(
        "\n========== STABLE DETECTOR =========="
    )

            print(
                "Detector:",
                detector,
            )

            print(
                "Detector ID:",
                id(detector),
            )

            print(
                "Input Prediction:",
                prediction,
            )

            print(
                "Input Confidence:",
                confidence,
            )


            # ------------------------------------------------
            # IMPORTANT:
            #
            # update() is called exactly ONCE.
            # ------------------------------------------------

            try:

                stable_prediction = (
                    detector.update(
                        prediction=prediction,
                        confidence=confidence,
                    )
                )

            except Exception as e:

                print(
                    "Stable Detector Error:",
                    e,
                )

                stable_prediction = {

                    "stable": False,

                    "prediction": None,

                    "confidence": 0.0,

                    "stable_frames": 0,

                    "unstable_frames": 0,

                    "required_frames": (
                        detector.required_stable_frames
                    ),

                    "gesture_stability": 0.0,

                    "majority_prediction": None,

                    "majority_ratio": 0.0,

                    "last_stable_prediction": (
                        detector.last_stable_prediction
                    ),

                    "new_stable": False,

                }


            # ------------------------------------------------
            # Ensure stable result is always a dictionary.
            # ------------------------------------------------

            if not isinstance(
                stable_prediction,
                dict,
            ):

                print(
                    "WARNING: Stable detector returned "
                    "non-dictionary result."
                )

                stable_prediction = {

                    "stable": False,

                    "prediction": None,

                    "confidence": 0.0,

                    "stable_frames": 0,

                    "unstable_frames": 0,

                    "required_frames": (
                        detector.required_stable_frames
                    ),

                    "gesture_stability": 0.0,

                    "majority_prediction": None,

                    "majority_ratio": 0.0,

                    "last_stable_prediction": (
                        detector.last_stable_prediction
                    ),

                    "new_stable": False,
                }


            # ------------------------------------------------
            # DEBUG STABLE RESULT
            # ------------------------------------------------

            print(
                "Stable Result:",
                stable_prediction,
            )

            print(
                "Stable:",
                stable_prediction.get(
                    "stable",
                    False,
                ),
            )

            print(
                "Stable Gesture:",
                stable_prediction.get(
                    "prediction"
                ),
            )

            print(
                "Stable Confidence:",
                stable_prediction.get(
                    "confidence",
                    0,
                ),
            )

            print(
                "Stable Frames:",
                stable_prediction.get(
                    "stable_frames",
                    0,
                ),
            )

            print(
                "Required Frames:",
                stable_prediction.get(
                    "required_frames",
                    detector.required_stable_frames,
                ),
            )

            print(
                "Gesture Stability:",
                stable_prediction.get(
                    "gesture_stability",
                    0,
                ),
            )

            print(
                "Majority Ratio:",
                stable_prediction.get(
                    "majority_ratio",
                    0,
                ),
            )

            print(
                "New Stable:",
                stable_prediction.get(
                    "new_stable",
                    False,
                ),
            )

            print(
                "===================================="
            )


        # ====================================================
        # 20. USE STABLE RESULT ONLY WHEN ACTUALLY STABLE
        # ====================================================

        if stable_prediction.get(
            "stable",
            False,
        ):

            stable_gesture = self.clean_prediction(
                stable_prediction.get(
                    "prediction",
                    prediction,
                )
            )

            stable_confidence = (
                self.normalize_confidence(
                    stable_prediction.get(
                        "confidence",
                        confidence,
                    )
                )
            )


            # -----------------------------------------------
            # Stable prediction becomes the session's latest
            # prediction.
            # -----------------------------------------------

            session["latest_prediction"] = (
                stable_gesture
            )

            session["latest_confidence"] = (
                stable_confidence
            )


        # ====================================================
        # 21. SAVE STABLE RESULT TO SESSION
        # ====================================================

        session[
            "latest_stable_prediction"
        ] = stable_prediction


        # ====================================================
        # 22. UPDATE STABILITY CALCULATOR
        # ====================================================

        if stability:

            try:

                stability.update(
                    prediction=prediction,
                    confidence=confidence,
                    stable=stable_prediction.get(
                        "stable",
                        False,
                    ),
                )

            except Exception as e:

                print(
                    "Stability Calculator Error:",
                    e,
                )


        # ====================================================
        # 23. BUILD MOTION METRICS
        # ====================================================

        motion_metrics = {}


        if motion:

            try:

                motion_metrics.update(
                    motion.get_metrics()
                )

            except Exception as e:

                print(
                    "Motion Metrics Error:",
                    e,
                )


        if stability:

            try:

                motion_metrics.update(
                    stability.get_metrics()
                )

            except Exception as e:

                print(
                    "Stability Metrics Error:",
                    e,
                )


        # ====================================================
        # 24. PERFORMANCE METRICS
        # ====================================================

        if monitor:

            try:

                performance = (
                    monitor.get_metrics()
                )

            except Exception as e:

                print(
                    "Performance Metrics Error:",
                    e,
                )

                performance = {}

        else:

            performance = {}


        # ====================================================
        # 25. BUFFER STATE
        # ====================================================

        if temporal_buffer:

            try:

                buffer_size = (
                    temporal_buffer.size()
                )

                buffer_full = (
                    temporal_buffer.is_full()
                )

            except Exception as e:

                print(
                    "Temporal Buffer State Error:",
                    e,
                )

                buffer_size = 0

                buffer_full = False

        else:

            buffer_size = 0

            buffer_full = False


        # ====================================================
        # 26. SAVE SESSION
        # ====================================================

        self.session_service.update_session(
            session_id,
            session,
        )


        # ====================================================
        # 27. FINAL FRAME DEBUG
        # ====================================================

        print(
            "\n========== FRAME RESULT =========="
        )

        print(
            "Raw Prediction:",
            prediction,
        )

        print(
            "Raw Confidence:",
            confidence,
        )

        print(
            "Stable:",
            stable_prediction.get(
                "stable",
                False,
            ),
        )

        print(
            "Stable Gesture:",
            stable_prediction.get(
                "prediction"
            ),
        )

        print(
            "Session Latest Prediction:",
            session.get(
                "latest_prediction"
            ),
        )

        print(
            "Session Latest Confidence:",
            session.get(
                "latest_confidence"
            ),
        )

        print(
            "=================================="
        )


        # ====================================================
        # 28. RETURN FRAME RESULT
        # ====================================================

        return {

            "success": True,

            "validation": validation,

            # ----------------------------------------------
            # Raw prediction
            # ----------------------------------------------

            "prediction": prediction,

            "confidence": round(
                confidence,
                3,
            ),

            "top_predictions": (
                top_predictions
            ),


            # ----------------------------------------------
            # Stable prediction
            # ----------------------------------------------

            "stable_prediction": (
                stable_prediction
            ),

            "stable": stable_prediction.get(
                "stable",
                False,
            ),

            "stable_gesture": (
                stable_prediction.get(
                    "prediction"
                )
            ),

            "stable_confidence": (
                self.normalize_confidence(
                    stable_prediction.get(
                        "confidence",
                        0,
                    )
                )
            ),

            "stable_frames": (
                stable_prediction.get(
                    "stable_frames",
                    0,
                )
            ),

            "required_frames": (
    stable_prediction.get(
        "required_frames",
        detector.required_stable_frames
        if detector is not None
        else 3,
    )
),

            "gesture_stability": (
                stable_prediction.get(
                    "gesture_stability",
                    0,
                )
            ),

            "new_stable": (
                stable_prediction.get(
                    "new_stable",
                    False,
                )
            ),


            # ----------------------------------------------
            # Buffer
            # ----------------------------------------------

            "buffer_size": buffer_size,

            "buffer_full": buffer_full,


            # ----------------------------------------------
            # Metrics
            # ----------------------------------------------

            "motion_metrics": motion_metrics,

            "performance": performance,
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
    motion_metrics=None
):
        print("\n========== RECORD ATTEMPT ==========")
        print("SESSION :", session_id)

        # --------------------------------------------------
        # Get Session
        # --------------------------------------------------

        session = self.session_service.get_session(
            session_id
        )

        if session is None:
            return {
                "success": False,
                "message": "Session not found."
            }

        # --------------------------------------------------
        # Basic Session Information
        # --------------------------------------------------

        student_id = session.get(
            "student_id",
            "default_student"
        )

        lesson_id = session.get("lesson_id")
        lesson = self.lesson_service.get_lesson_by_id(
    db,
    lesson_id
)
        if lesson and lesson.sign:
            expected = self.clean_prediction(
        lesson.sign
    )
        else:
            expected = self.clean_prediction(
        session.get(
            "current_letter",
            "A"
        )
    )
            if expected == "COMPLETED":
                expected = self.clean_prediction(
            session.get(
                "selected_letter",
                "A"
            )
        )
            if expected == "COMPLETED":
                expected = self.clean_prediction(
        session.get(
            "selected_letter",
            "A"
        )
    )

        # --------------------------------------------------
        # Stored Prediction From Frame Processing
        # --------------------------------------------------

        stored_prediction = self.clean_prediction(
            session.get(
                "latest_prediction",
                "UNKNOWN"
            )
        )

        stored_confidence = self.normalize_confidence(
            session.get(
                "latest_confidence",
                0
            )
        )

        stored_stable = session.get(
            "latest_stable_prediction",
            {}
        )

        # --------------------------------------------------
        # Determine Final Prediction
        # --------------------------------------------------

        final_prediction = stored_prediction
        final_confidence = stored_confidence

        # Stable prediction has highest priority
        if (
            stored_stable
            and stored_stable.get("stable")
            and stored_stable.get("prediction")
        ):
            final_prediction = self.clean_prediction(
                stored_stable.get(
                    "prediction"
                )
            )

            final_confidence = self.normalize_confidence(
                stored_stable.get(
                    "confidence",
                    stored_confidence
                )
            )

        # --------------------------------------------------
        # Use Passed Stable Prediction If Available
        # --------------------------------------------------

        if stable_prediction is None:
            stable_prediction = stored_stable

        if (
            stable_prediction
            and stable_prediction.get(
                "stable",
                False
            )
            and stable_prediction.get(
                "prediction"
            )
        ):
            final_prediction = self.clean_prediction(
                stable_prediction.get(
                    "prediction"
                )
            )

            final_confidence = self.normalize_confidence(
                stable_prediction.get(
                    "confidence",
                    stored_confidence
                )
            )

        # --------------------------------------------------
        # Fallback Prediction
        # --------------------------------------------------
        # Only predict again if there is no usable
        # prediction already available.

        elif (
            final_prediction in (
                None,
                "",
                "UNKNOWN"
            )
            and landmarks
            and len(landmarks) == 21
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

            except Exception as e:
                print(
                    "Final Prediction Error :",
                    e
                )

                final_prediction = "UNKNOWN"
                final_confidence = 0.0

        # --------------------------------------------------
        # Final Normalization
        # --------------------------------------------------

        final_prediction = self.clean_prediction(
            final_prediction
        )

        final_confidence = self.normalize_confidence(
            final_confidence
        )

        # --------------------------------------------------
        # Correct / Incorrect
        # --------------------------------------------------

        correct = (
            expected == final_prediction
        )

        print(
            "EXPECTED   :",
            expected
        )

        print(
            "PREDICTED  :",
            final_prediction
        )

        print(
            "CORRECT    :",
            correct
        )

        print(
            "CONFIDENCE :",
            final_confidence
        )

        # --------------------------------------------------
        # Validate Final Landmarks
        # --------------------------------------------------

        if (
            landmarks
            and len(landmarks) == 21
        ):
            validation = self.frame_validator.validate(
                landmarks=landmarks,
                hand_count=1,
                person_count=1,
                body_visible=True
            )

        else:
            validation = {
                "valid": True,
                "reason": "USING_STORED_PREDICTION"
            }

        # --------------------------------------------------
        # Merge Motion Metrics
        # --------------------------------------------------

        final_motion = {}

        # Motion metrics sent by API request
        if motion_metrics:
            final_motion.update(
                motion_metrics
            )

        # Runtime motion metrics collected
        # during frame processing
        runtime_motion = self.motion_metrics.get(
            session_id
        )

        if runtime_motion:
            final_motion.update(
                runtime_motion.get_metrics()
            )

        # Stability metrics collected
        # during frame processing
        stability_calculator = (
            self.stability_calculators.get(
                session_id
            )
        )

        if stability_calculator:
            final_motion.update(
                stability_calculator.get_metrics()
            )

        print(
            "\n========== FINAL MOTION METRICS =========="
        )

        print(
            final_motion
        )

        # --------------------------------------------------
        # Generate Assessment ID
        # --------------------------------------------------

        assessment_id = str(
            uuid.uuid4()
        )[:8].upper()

        # --------------------------------------------------
        # Generate Feedback
        # --------------------------------------------------

        try:
            feedback = self.feedback_engine.evaluate(
                expected=expected,
                predicted=final_prediction,
                confidence=final_confidence,
                landmarks=landmarks,
                validation_reason=validation.get(
                    "reason"
                ),
                stable_prediction=stable_prediction,
                motion_metrics=final_motion
            )

        except Exception as e:
            print(
                "Feedback Error :",
                e
            )

            feedback = {
                "message":
                    "Unable to generate detailed feedback.",
                "error":
                    str(e)
            }

        # --------------------------------------------------
        # Calculate Sign Score
        # --------------------------------------------------

        try:
            sign_score = (
                self.score_calculator.calculate(
                    correct=correct,
                    confidence=(
                        final_confidence * 100
                    ),
                    stability=(
                        final_motion.get(
                            "gesture_stability",
                            0
                        )
                    ),
                    time_taken=(
                        final_motion.get(
                            "time_taken",
                            0
                        )
                    )
                )
            )

        except Exception as e:
            print(
                "Sign Score Error :",
                e
            )

            sign_score = {
                "overall_score": 0,
                "grade":
                    "Needs Improvement",
                "components": {}
            }

        # --------------------------------------------------
        # Build Attempt Data
        # --------------------------------------------------

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
                datetime.now().isoformat()
        }

        print(
            "\n========== ATTEMPT DATA CREATED =========="
        )

        print(
            "Assessment ID :",
            assessment_id
        )

        print(
            "Student       :",
            student_id
        )

        print(
            "Expected      :",
            expected
        )

        print(
            "Predicted     :",
            final_prediction
        )

        print(
            "Correct       :",
            correct
        )

        print(
            "Confidence    :",
            final_confidence
        )

        # --------------------------------------------------
        # Save Assessment History
        # --------------------------------------------------
        # Save the complete attempt only after
        # feedback, score, and attempt data are ready.

        self.assessment_history.add_attempt(
            attempt_data
        )

        print(
            "\n========== ASSESSMENT HISTORY UPDATED =========="
        )

        print(
            "Assessment ID :",
            assessment_id
        )

        # --------------------------------------------------
        # Update Learner Profile
        # --------------------------------------------------
        # This is the only place where the learner's
        # alphabet-learning progression is changed.

        profile = (
            self.learner_profile_service.update_after_attempt(
                student_id=student_id,
                alphabet=expected,
                predicted=final_prediction,
                confidence=final_confidence,
                correct=correct
            )
        )
        

        # --------------------------------------------------
        # Validate Profile Response
        # --------------------------------------------------

        if profile is None:
            profile = {
                "student_id":
                    student_id,

                "completed_letters":
                    [],

                "current_letter":
                    expected,

                "next_letter":
                    None
            }

        # --------------------------------------------------
        # Sync Profile Progress Into Attempt
        # --------------------------------------------------

        attempt_data["completed_letters"] = (
            profile.get(
                "completed_letters",
                []
            )
        )

        attempt_data["current_letter"] = (
            profile.get(
                "current_letter",
                expected
            )
        )

        attempt_data["next_letter"] = (
            profile.get(
                "next_letter"
            )
        )

        # --------------------------------------------------
        # Learning State
        # --------------------------------------------------

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

        except Exception as e:
            print(
                "Learning State Error :",
                e
            )

            learning_state = {}

        # --------------------------------------------------
        # Error Analysis
        # --------------------------------------------------

        try:
            analysis = (
                self.error_analysis_service.analyze_student(
                    student_id
                )
            )

        except Exception as e:
            print(
                "Error Analysis Error :",
                e
            )

            analysis = {}

        performance_trends = (
            analysis.get(
                "performance_trends",
                []
            )
        )

        # --------------------------------------------------
        # Confusion Analysis
        # --------------------------------------------------

        try:
            confusion_pairs = self._get_confusions(
                profile
            )

        except Exception as e:
            print(
                "Confusion Analysis Error :",
                e
            )

            confusion_pairs = {}

        print(
            "\n========== LEARNING PROGRESS =========="
        )

        print(
            "Completed Letters :",
            profile.get(
                "completed_letters",
                []
            )
        )

        print(
            "Current Letter    :",
            profile.get(
                "current_letter"
            )
        )

        print(
            "Next Letter       :",
            profile.get(
                "next_letter"
            )
        )

        print(
            "Performance Trends:",
            performance_trends
        )

        print(
            "Confusion Pairs   :",
            confusion_pairs
        )

        # --------------------------------------------------
        # Recommendation Engine
        # --------------------------------------------------

        try:
            recommendations = (
                self.recommendation_engine.generate(
                    learner_profile=profile,
                    confusion_pairs=confusion_pairs,
                    trends=performance_trends
                )
            )

        except Exception as e:
            print(
                "Recommendation Engine Error :",
                e
            )

            recommendations = []

        # --------------------------------------------------
        # Default Recommendation
        # --------------------------------------------------

        if not recommendations:
            next_letter = profile.get(
                "next_letter"
            )

            if (
                next_letter
                and next_letter != "COMPLETED"
            ):
                recommendations.append(
                    {
                        "alphabet":
                            next_letter,

                        "reason":
                            "Continue sequential learning.",

                        "priority":
                            "HIGH"
                    }
                )

        print(
            "\n========== RECOMMENDATIONS =========="
        )

        print(
            recommendations
        )

        # --------------------------------------------------
        # Update Practice Queue
        # --------------------------------------------------

        try:
            self.practice_queue.update_queue(
                student_id,
                recommendations
            )

        except Exception as e:
            print(
                "Practice Queue Error :",
                e
            )

        # --------------------------------------------------
        # Get Next Practice
        # --------------------------------------------------

        try:
            next_practice = (
                self.practice_queue.get_next_practice(
                    student_id
                )
            )

        except Exception as e:
            print(
                "Next Practice Error :",
                e
            )

            next_practice = None

        # --------------------------------------------------
        # Recommended Letter
        # --------------------------------------------------

        recommended_letter = None

        if next_practice:
            recommended_letter = (
                next_practice.get(
                    "alphabet"
                )
            )

        # --------------------------------------------------
        # Dashboard
        # --------------------------------------------------

        

        # --------------------------------------------------
        # Record Attempt In SessionService
        # --------------------------------------------------
        #
        # SessionService.record_attempt() is the ONLY
        # place responsible for:
        #
        # - history
        # - attempts
        # - correct_attempts
        # - incorrect_attempts
        # - accuracy
        # - letter_attempts
        # - mastery
        #
        # DO NOT manually update those values here.
        # --------------------------------------------------

        updated_session = (
            self.session_service.record_attempt(
                session_id,
                attempt_data
            )
        )

        if updated_session is None:
            print(
                "SessionService could not update session."
            )

            return {
                "success": False,
                "message":
                    "Unable to record practice attempt."
            }

        session = updated_session

        # --------------------------------------------------
        # Synchronize Learner Profile With Session
        # --------------------------------------------------

        session["completed_letters"] = (
            profile.get(
                "completed_letters",
                []
            ).copy()
        )

        session["current_letter"] = (
            profile.get(
                "current_letter",
                session.get(
                    "current_letter",
                    expected
                )
            )
        )

        session["next_letter"] = (
            profile.get(
                "next_letter",
                session.get(
                    "next_letter"
                )
            )
        )

        # --------------------------------------------------
        # Remaining Letters
        # --------------------------------------------------

        completed_letters = set(
            session.get(
                "completed_letters",
                []
            )
        )

        session["remaining_letters"] = [
            letter
            for letter in self.session_service.alphabets
            if letter not in completed_letters
        ]

        # --------------------------------------------------
        # Store Updated Session
        # --------------------------------------------------

        self.session_service.update_session(
            session_id,
            session
        )


        print(
            "\n========== SESSION UPDATED =========="
        )

        print(
            "Attempts :",
            session.get(
                "attempts",
                0
            )
        )

        print(
            "Correct  :",
            session.get(
                "correct_attempts",
                0
            )
        )

        print(
            "Incorrect:",
            session.get(
                "incorrect_attempts",
                0
            )
        )

        print(
            "Accuracy :",
            session.get(
                "accuracy",
                0
            )
        )

        print(
            "Completed:",
            session.get(
                "completed_letters",
                []
            )
        )

        print(
            "Current  :",
            session.get(
                "current_letter"
            )
        )

        print(
            "Next     :",
            session.get(
                "next_letter"
            )
        )

        print(
            "Recommended:",
            recommended_letter
        )
        try:
            dashboard = self.dashboard_service.get_dashboard(
        student_id
    )
        except Exception as e:
            print(
        "Dashboard Error :",
        e
    )
        dashboard = {}
        print( "\n========== UPDATED DASHBOARD ==========")
        print(dashboard)

        # --------------------------------------------------
        # Final Response
        # --------------------------------------------------

        return {
            "success": True,

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
                    correct
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
                    next_practice
            },

            "dashboard":
                dashboard
        }

    # ==================================================
    # DASHBOARD
    # ==================================================

    def get_dashboard(
        self,
        student_id: str
    ):
        return self.dashboard_service.get_dashboard(
            student_id
        )
        # ==================================================
    # LEARNER PROFILE
    # ==================================================

    def get_learner_profile(
        self,
        student_id: str
    ):
        return self.learner_profile_service.get_profile(
            student_id
        )


    # ==================================================
    # ASSESSMENT HISTORY
    # ==================================================

    def get_student_assessments(
        self,
        student_id: str
    ):
        return self.assessment_history.get_student_history(
            student_id
        )


    def get_session_assessments(
        self,
        session_id: str
    ):
        return self.assessment_history.get_session_history(
            session_id
        )


    def get_assessment_history(self):
        return self.assessment_history.get_all()


    # ==================================================
    # ERROR ANALYSIS
    # ==================================================

    def get_error_analysis(
        self,
        student_id: str
    ):
        return self.error_analysis_service.analyze_student(
            student_id
        )
    def get_student_report(
    self,
    student_id: str
):
        return self.report_service.get_student_report(
        student_id
    )