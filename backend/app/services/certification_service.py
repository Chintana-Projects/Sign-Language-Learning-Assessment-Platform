import uuid
import string
from datetime import datetime
from app.database.certificate_database import (
    CertificateDatabase
)
from app.services.notification_service import NotificationService
from app.certification.certification_session import (
    CertificationSession
)
from app.ai.temporal.temporal_buffer import (
    TemporalBuffer
)
from app.ai.temporal.stable_detector import (
    StableGestureDetector
)
from app.ai.temporal.stability_calculator import (
    StabilityCalculator
)
from app.learning.motion_metrics import (
    MotionMetrics
)
from app.ai.performance.performance_monitor import (
    PerformanceMonitor
)


class CertificationService:

    def __init__(
        self,
        assessment_service=None,
        learner_profile_service=None
    ):
        print("USING app/services/certification_service.py")
        self.assessment_service = (
            assessment_service
        )
        self.learner_profile_service = (
            learner_profile_service
        )
        self.notification_service = NotificationService()
        self.certificate_db = (
    CertificateDatabase()
)
        self.session_manager = (
            CertificationSession()
        )
        self.letters = list(
            string.ascii_uppercase
        )
        self.sessions = {}

    # =====================================================
    # START CERTIFICATION
    # =====================================================

    def start_certification(
        self,
        student_id="test_student"
    ):
       
        certification_id = str(
            uuid.uuid4()
        )

        session = {
            "certification_id": certification_id,
            "student_id": student_id,
            "current_index": 0,
            "current_letter": "A",
            "status": "in_progress",
            "score": 0,
            "passed": False,
            "results": []
        }

        # -----------------------------------------
        # Certification session
        # -----------------------------------------

        self.sessions[
            certification_id
        ] = session

        # -----------------------------------------
        # Assessment session
        # -----------------------------------------

        self.assessment_service.session_service.sessions[
            certification_id
        ] = {
            "session_id": certification_id,
            "student_id": student_id,
            "current_letter": "A",
            "completed_letters": [],
            "latest_prediction": None,
            "latest_confidence": 0.0,
            "latest_stable_prediction": {
                "stable": False,
                "prediction": None,
                "confidence": 0.0,
                "stable_frames": 0,
                "unstable_frames": 0
            }
        }

        # -----------------------------------------
        # Runtime components
        # -----------------------------------------

        self.assessment_service.temporal_buffers[
            certification_id
        ] = TemporalBuffer(
            max_frames=30
        )

        self.assessment_service.stable_detectors[
            certification_id
        ] = StableGestureDetector(
            required_stable_frames=3,
            confidence_threshold=0.10,
            stability_threshold=60,
            history_size=5,
        )

        self.assessment_service.stability_calculators[
            certification_id
        ] = StabilityCalculator()

        self.assessment_service.motion_metrics[
            certification_id
        ] = MotionMetrics()

        self.assessment_service.performance_monitors[
            certification_id
        ] = PerformanceMonitor()

        return {
            "success": True,
            "message": "Certification started",
            "certification_id": certification_id,
            "current_letter": "A",
            "progress": 0,
            "total_letters": 26
        }

    # =====================================================
    # PROCESS FRAME
    # =====================================================

    def process_frame(
        self,
        certification_id,
        landmarks,
        hand_count=1,
        person_count=1,
        body_visible=True
    ):
        session = self.sessions.get(
            certification_id
        )

        if session is None:
            return {
                "success": False,
                "message": "Certification session not found."
            }

        return self.assessment_service.process_frame(
            session_id=certification_id,
            landmarks=landmarks,
            hand_count=hand_count,
            person_count=person_count,
            body_visible=body_visible
        )

    # =====================================================
    # GET SESSION
    # =====================================================

    def get_session(
        self,
        certification_id
    ):
        return self.sessions.get(
            certification_id
        )

    # =====================================================
    # SUBMIT LETTER
    # =====================================================

    def submit_letter(
        self,
        certification_id,
        predicted_letter,
        confidence=1.0
    ):
        session = self.sessions.get(
            certification_id
        )

        if session is None:
            return {
                "success": False,
                "message": "Certification session not found."
            }

        current_letter = session[
            "current_letter"
        ]

        correct = (
            predicted_letter.upper()
            ==
            current_letter.upper()
        )

        session["results"].append({
            "letter": current_letter,
            "predicted": predicted_letter,
            "confidence": confidence,
            "correct": correct
        })

        if correct:
            session["score"] += 1

        session["current_index"] += 1

        # ==========================================
        # CERTIFICATION COMPLETE
        # ==========================================

        if session["current_index"] >= 26:

            percentage = round(
                (session["score"] / 26) * 100,
                2
            )

            session["status"] = "completed"

            session["passed"] = (
                percentage >= 60
            )

            certificate_id = None

            if session["passed"]:

                certificate_id = (
                    f"CERT-{session['student_id']}-"
                    f"{uuid.uuid4().hex[:6].upper()}"
                )

                session["certificate_id"] = (
                    certificate_id
                )

                if self.learner_profile_service:

                    profile = (
                        self.learner_profile_service
                        .get_profile(
                            session["student_id"]
                        )
                    )

                    profile["certified"] = True

                    profile["certified_at"] = (
                        datetime.now().isoformat()
                    )

                    profile["certificate_id"] = (
                        certificate_id
                    )

                    if percentage >= 86:
                         level = "Professional"
                         badge = "👑"
                    elif percentage >= 71:
                         level = "Intermediate"
                         badge = "🥈"
                    else:
                         level = "Beginner"
                         badge = "📘"

                    profile["certification_level"] = level
                    profile["certificate_id"] = certificate_id


                    profile[
                        "completed_letters"
                    ] = [
                        chr(i)
                        for i in range(
                            ord("A"),
                            ord("Z") + 1
                        )
                    ]
                    profile["lesson_progress"] = {

    "completed": 26,

    "total": 26,

    "percentage": 100.0
}

                    profile[
                        "current_letter"
                    ] = "COMPLETED"

                    profile[
                        "next_letter"
                    ] = "COMPLETED"

                    profile[
                        "overall_accuracy"
                    ] = percentage
                    print("SAVING CERTIFICATE...")
                    print("Certificate ID:", certificate_id)
                    self.certificate_db.add_certificate({

    "certificate_id":
        certificate_id,

    "badge": badge,

    "student_id":
        session["student_id"],

    "student_name":
        profile.get(
            "student_name",
            session["student_id"]
        ),

    "score":
        percentage,

    "level":
        level,

    "issued_at":
        datetime.now().isoformat()

})
                    print("CERTIFICATE SAVED")

                    self.learner_profile_service.save_profiles()

            return {
                "success": True,
                "completed": True,
                "score": percentage,
                "passed": session["passed"],
                "certificate_id": certificate_id,
                "correct_answers": session["score"],
                "total_questions": 26,
                "certificate_eligible": session["passed"],
                "results": session["results"],
                "message": "Certification completed."
            }

        # ==========================================
        # NEXT LETTER
        # ==========================================

        next_letter = chr(
            ord("A")
            +
            session["current_index"]
        )

        session[
            "current_letter"
        ] = next_letter

        assessment_session = (
            self.assessment_service
            .session_service
            .get_session(
                certification_id
            )
        )

        if assessment_session:
            assessment_session[
                "current_letter"
            ] = next_letter

            self.assessment_service.session_service.update_session(
                certification_id,
                assessment_session
            )

        return {
            "success": True,
            "completed": False,
            "current_letter": next_letter,
            "progress": session["current_index"],
            "remaining": 26 - session["current_index"]
        }

    # =====================================================
    # RESULTS
    # =====================================================

    def get_results(
        self,
        certification_id
    ):
        session = self.sessions.get(
            certification_id
        )

        if session is None:
            return {
                "success": False,
                "message": "Certification session not found."
            }

        return {
            "success": True,
            "certification_id": certification_id,
            "status": session["status"],
            "score": round(
                (session["score"] / 26) * 100,
                2
            ),
            "passed": session["passed"],
            "results": session["results"],
            "completed_letters": [
                result["letter"]
                for result in session["results"]
            ]
        }