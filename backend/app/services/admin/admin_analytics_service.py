from collections import Counter
from datetime import datetime, timedelta

from app.assessment.assessment_history import AssessmentHistory
from app.services.learner.learner_profile_service import (
    LearnerProfileService,
)


class AdminAnalyticsService:

    def __init__(self):

        self.assessment_history = AssessmentHistory()

        self.profile_service = LearnerProfileService()

    # =====================================================
    # PLATFORM STATISTICS
    # =====================================================

    def get_platform_statistics(self):

        attempts = self.assessment_history.get_all()

        total_assessments = len(attempts)

        total_correct = sum(
            1 for a in attempts
            if a.get("correct", False)
        )

        average_accuracy = (
            (total_correct / total_assessments) * 100
            if total_assessments > 0
            else 0
        )

        confidences = [
            float(a.get("confidence", 0))
            for a in attempts
        ]

        average_confidence = (
            (sum(confidences) / len(confidences)) * 100
            if confidences
            else 0
        )

        unique_students = set(
            a.get("student_id")
            for a in attempts
            if a.get("student_id")
        )

        return {

            "total_users":
                len(unique_students),

            "total_learners":
                len(unique_students),

            "total_trainers":
                0,

            "total_admins":
                1,

            "total_assessments":
                total_assessments,

            "average_accuracy":
                round(
                    average_accuracy,
                    2
                ),

            "average_confidence":
                round(
                    average_confidence,
                    2
                ),
        }

    # =====================================================
    # USER GROWTH
    # =====================================================

    def get_user_growth(self):

        attempts = self.assessment_history.get_all()

        growth = {}

        for attempt in attempts:

            timestamp = attempt.get(
                "timestamp"
            )

            if not timestamp:
                continue

            try:

                date = datetime.fromisoformat(
                    timestamp
                ).strftime(
                    "%Y-%m-%d"
                )

                growth[date] = (
                    growth.get(
                        date,
                        0
                    ) + 1
                )

            except Exception:
                pass

        return [

            {
                "date": date,
                "count": count
            }

            for date, count in sorted(
                growth.items()
            )
        ]

    # =====================================================
    # ACCURACY TREND
    # =====================================================

    def get_accuracy_trends(self):

        attempts = self.assessment_history.get_all()

        daily = {}

        for attempt in attempts:

            timestamp = attempt.get(
                "timestamp"
            )

            if not timestamp:
                continue

            try:

                date = datetime.fromisoformat(
                    timestamp
                ).strftime(
                    "%Y-%m-%d"
                )

                if date not in daily:

                    daily[date] = []

                daily[date].append(
                    100
                    if attempt.get(
                        "correct"
                    )
                    else 0
                )

            except Exception:
                pass

        result = []

        for date, scores in sorted(
            daily.items()
        ):

            result.append({

                "date":
                    date,

                "accuracy":
                    round(
                        sum(scores)
                        / len(scores),
                        2
                    )
            })

        return result

    # =====================================================
    # ASSESSMENT ACTIVITY
    # =====================================================

    def get_assessment_activity(self):

        attempts = self.assessment_history.get_all()

        activity = {}

        for attempt in attempts:

            timestamp = attempt.get(
                "timestamp"
            )

            if not timestamp:
                continue

            try:

                date = datetime.fromisoformat(
                    timestamp
                ).strftime(
                    "%Y-%m-%d"
                )

                activity[date] = (
                    activity.get(
                        date,
                        0
                    ) + 1
                )

            except Exception:
                pass

        return [

            {
                "date": date,
                "assessments": count
            }

            for date, count in sorted(
                activity.items()
            )
        ]

    # =====================================================
    # ROLE DISTRIBUTION
    # =====================================================

    def get_role_distribution(self):

        stats = self.get_platform_statistics()

        return [

            {
                "name": "Learners",
                "value": stats[
                    "total_learners"
                ]
            },

            {
                "name": "Trainers",
                "value": stats[
                    "total_trainers"
                ]
            },

            {
                "name": "Admins",
                "value": stats[
                    "total_admins"
                ]
            }
        ]

    # =====================================================
    # MOST PRACTICED LETTER
    # =====================================================

    def get_most_practiced_letter(self):

        attempts = self.assessment_history.get_all()

        letters = [

            a.get("expected")

            for a in attempts

            if a.get("expected")
        ]

        if not letters:

            return None

        return Counter(
            letters
        ).most_common(1)[0][0]

    # =====================================================
    # MOST CONFUSED PAIR
    # =====================================================

    def get_most_confused_pair(self):

        attempts = self.assessment_history.get_all()

        pairs = []

        for a in attempts:

            if a.get("correct"):
                continue

            expected = a.get(
                "expected"
            )

            predicted = a.get(
                "predicted"
            )

            if expected and predicted:

                pairs.append(
                    f"{expected} → {predicted}"
                )

        if not pairs:

            return None

        return Counter(
            pairs
        ).most_common(1)[0][0]

    # =====================================================
    # FULL ANALYTICS RESPONSE
    # =====================================================

    def get_dashboard_analytics(self):

        stats = self.get_platform_statistics()

        stats.update({

            "user_growth":
                self.get_user_growth(),

            "accuracy_trends":
                self.get_accuracy_trends(),

            "assessment_activity":
                self.get_assessment_activity(),

            "role_distribution":
                self.get_role_distribution(),

            "most_practiced_letter":
                self.get_most_practiced_letter(),

            "most_confused_pair":
                self.get_most_confused_pair(),
        })

        return stats