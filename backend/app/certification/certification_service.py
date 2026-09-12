# app/certification/certification_service.py

from datetime import datetime
import string
import uuid

from app.certification.certification_session import (
    CertificationSession
)


class CertificationService:

    PASSING_SCORE = 60

    def __init__(
    self,
    assessment_service=None,
    learner_profile_service=None
):
        print("USING app/certification/certification_service.py")
        self.assessment_service = (
        assessment_service
    )
        self.learner_profile_service = (
        learner_profile_service
    )
        self.session_manager = (
        CertificationSession()
    )
        self.letters = list(
        string.ascii_uppercase
    )

    # ============================================================
    # START CERTIFICATION
    # ============================================================

    def start_certification(
        self,
        student_id: str
    ):
        profile = (
    self.learner_profile_service
    .get_profile(student_id)
)
        completed_letters = profile.get(
    "completed_letters",
    []
)
        if len(completed_letters) < 26:
            return {

        "success": False,

        "locked": True,

        "message":
            "Complete all 26 practice letters before certification.",

        "completed":
            len(completed_letters),

        "required":
            26
    }

        session = (
            self.session_manager.create_session(
                student_id
            )
        )

        return {

            "success": True,

            "message":
                "Certification started",

            "certification_id":
                session["certification_id"],

            "current_letter":
                session["current_letter"],

            "progress": 0,

            "total_letters": 26
        }

    # ============================================================
    # GET SESSION
    # ============================================================

    def get_session(
        self,
        certification_id: str
    ):

        return (
            self.session_manager.get_session(
                certification_id
            )
        )

    # ============================================================
    # SUBMIT LETTER
    # ============================================================

    def submit_letter(
        self,
        certification_id: str,
        predicted_letter: str,
        confidence: float = 0
    ):

        session = (
            self.session_manager.get_session(
                certification_id
            )
        )

        if session is None:

            return {

                "success": False,

                "message":
                    "Certification session not found."
            }

        if session.get("status") == "completed":

            return {

                "success": False,

                "message":
                    "Certification already completed."
            }

        expected_letter = (
            session["current_letter"]
        )

        predicted_letter = str(
            predicted_letter
        ).upper().strip()

        correct = (
            predicted_letter
            ==
            expected_letter
        )

        session["results"].append({

            "letter":
                expected_letter,

            "predicted":
                predicted_letter,

            "confidence":
                confidence,

            "correct":
                correct
        })

        session["completed_letters"].append(
            expected_letter
        )

        current_index = (
            self.letters.index(
                expected_letter
            )
        )

        # =====================================================
        # CERTIFICATION COMPLETE
        # =====================================================

        if current_index == len(self.letters) - 1:

            session["status"] = "completed"

            total_correct = sum(

                1

                for result in session["results"]

                if result["correct"]

            )

            score = round(

                (
                    total_correct
                    /
                    len(self.letters)
                ) * 100,

                2
            )

            passed = (
                score >= self.PASSING_SCORE
            )

            session["score"] = score
            session["passed"] = passed

            certificate_id = None

            if passed:
                certificate_id = str(
        uuid.uuid4()
    )[:8].upper()
                session["certificate_id"] = (
        certificate_id
    )
                if self.assessment_service:
                    profile_service = (
            self.assessment_service
            .learner_profile_service
        )
                    profile = (
            profile_service.get_profile(
                session["student_id"]
            )
        )
                profile["completed_letters"] = (
            self.letters.copy()
        )
                profile["current_letter"] = (
            "COMPLETED"
        )
                profile["next_letter"] = (
            "COMPLETED"
        )
                if score >= 86:
                    level = "Professional"
                elif score >= 71:
                    level = "Intermediate"
                elif score >= 60:
                    level = "Beginner"
                else:
                    level = None
                profile["certified"] = True
                profile["certification_level"] = (
            level
        )
                profile["certificate_id"] = (
            certificate_id
        )
                profile["certified_at"] = (
            datetime.now().isoformat()
        )
                self.notification_service.add_notification(
    student_id=session["student_id"],
    title="Certification Earned",
    message=f"You achieved {level} certification with a score of {score}%",
    notification_type="certification"
)
                notifications = profile.get(
    "notifications",
    []
)
                notifications.append({
    "id": str(uuid.uuid4()),
    "title": "Certification Earned 🎉",
    "message": f"You earned a {level} certification with a score of {score}%",
    "type": "certificate",
    "created_at": datetime.now().isoformat(),
    "read": False
})
                profile["notifications"] = notifications
                profile_service.save_profiles()

            return {

                "success": True,

                "completed": True,

                "score": score,

                "passed": passed,

                "certificate_id":
                    certificate_id,

                "correct_answers":
                    total_correct,

                "total_questions":
                    len(self.letters),

                "certificate_eligible":
                    passed,

                "results":
                    session["results"],

                "message":
                    "Certification completed."
            }

        # =====================================================
        # NEXT LETTER
        # =====================================================

        next_letter = self.letters[
            current_index + 1
        ]

        session["current_letter"] = (
            next_letter
        )

        progress = len(
            session["completed_letters"]
        )

        return {

            "success": True,

            "completed": False,

            "current_letter":
                next_letter,

            "progress":
                progress,

            "remaining":
                len(self.letters)
                - progress
        }

    # ============================================================
    # GET RESULTS
    # ============================================================

    def get_results(
        self,
        certification_id: str
    ):

        session = (
            self.session_manager.get_session(
                certification_id
            )
        )

        if session is None:

            return {

                "success": False,

                "message":
                    "Certification session not found."
            }

        return {

            "success": True,

            "certification_id":
                certification_id,

            "status":
                session.get(
                    "status"
                ),

            "score":
                session.get(
                    "score",
                    0
                ),

            "passed":
                session.get(
                    "passed",
                    False
                ),

            "results":
                session.get(
                    "results",
                    []
                ),

            "completed_letters":
                session.get(
                    "completed_letters",
                    []
                ),

            "certificate_id":
                session.get(
                    "certificate_id"
                )
        }