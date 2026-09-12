from datetime import datetime

from app.assessment.assessment_history import (
    AssessmentHistory,
)

from app.services.session_service import (
    SessionService,
)


class AdminMonitoringService:

    def __init__(self):

        self.history = AssessmentHistory()

        self.sessions = SessionService()

        self.start_time = datetime.now()

    def get_system_metrics(self):

        attempts = self.history.get_all()

        total_assessments = len(attempts)

        if total_assessments > 0:

            avg_confidence = round(

                sum(
                    a.get("confidence", 0)
                    for a in attempts
                ) / total_assessments * 100,

                2
            )

            accuracy = round(

                sum(
                    1
                    for a in attempts
                    if a.get("correct")
                )
                / total_assessments
                * 100,

                2
            )

        else:

            avg_confidence = 0
            accuracy = 0

        active_sessions = len(
            self.sessions.sessions
        )

        uptime = str(
            datetime.now() - self.start_time
        )

        return {

            "total_assessments":
                total_assessments,

            "average_accuracy":
                accuracy,

            "average_confidence":
                avg_confidence,

            "active_sessions":
                active_sessions,

            "uptime":
                uptime,

            "system_status":
                "Healthy"
        }