class LearnerAnalyticsService:

    def __init__(
        self,
        assessment_service
    ):
        self.assessment_service = assessment_service

    def generate_profile(
        self,
        student_id
    ):

        history = (
            self.assessment_service
            .assessment_history
            .get_student_history(
                student_id
            )
        )

        # =====================================
        # No Practice History
        # =====================================

        if not history:

            return {
                "student_id": student_id,
                "total_attempts": 0,
                "accuracy": 0.0,
                "learning_level": "Beginner",
                "strong_gestures": [],
                "weak_gestures": [],
                "recommendations": [],
                "message": "No practice history available."
            }

        # =====================================
        # Overall Statistics
        # =====================================

        total = len(history)

        correct = sum(
            1
            for item in history
            if item.get("correct", False)
        )

        accuracy = round(
            (correct / total) * 100,
            2
        )

        # =====================================
        # Gesture Statistics
        # =====================================

        gesture_stats = {}

        for item in history:

            letter = item.get("expected")

            if not letter:
                continue

            gesture_stats.setdefault(
                letter,
                {
                    "correct": 0,
                    "total": 0
                }
            )

            gesture_stats[letter]["total"] += 1

            if item.get("correct", False):

                gesture_stats[letter]["correct"] += 1

        # =====================================
        # Weak / Strong Gestures
        # =====================================

        weak = []
        strong = []

        for letter, data in gesture_stats.items():

            if data["total"] == 0:
                continue

            score = (
                data["correct"]
                / data["total"]
            ) * 100

            if score < 60:

                weak.append(letter)

            elif score >= 90:

                strong.append(letter)

        # =====================================
        # Learning Level
        # =====================================

        if accuracy >= 90:

            level = "Mastered"

        elif accuracy >= 70:

            level = "Good"

        elif accuracy >= 40:

            level = "Improving"

        else:

            level = "Beginner"

        # =====================================
        # Recommendations
        # =====================================

        recommendations = []

        if weak:

            recommendations.append({
                "type": "PRACTICE",
                "priority": "HIGH",
                "message":
                    "Practice weak gestures: "
                    + ", ".join(weak)
            })

        if level == "Beginner":

            recommendations.append({
                "type": "FOUNDATION",
                "priority": "HIGH",
                "message":
                    "Continue basic alphabet "
                    "practice to improve consistency."
            })

        elif level == "Improving":

            recommendations.append({
                "type": "CONSISTENCY",
                "priority": "NORMAL",
                "message":
                    "Keep practicing regularly "
                    "to improve recognition accuracy."
            })

        elif level == "Good":

            recommendations.append({
                "type": "ADVANCED",
                "priority": "NORMAL",
                "message":
                    "Good progress. Practice "
                    "confusing letters to improve accuracy."
            })

        else:

            recommendations.append({
                "type": "MAINTENANCE",
                "priority": "LOW",
                "message":
                    "Excellent work. Continue "
                    "practicing to maintain mastery."
            })

        # =====================================
        # RETURN PROFILE
        # =====================================

        return {

            "student_id": student_id,

            "total_attempts": total,

            "accuracy": accuracy,

            "learning_level": level,

            "strong_gestures": strong,

            "weak_gestures": weak,

            "recommendations": recommendations

        }