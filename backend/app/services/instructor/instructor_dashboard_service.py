from statistics import mean


class InstructorDashboardService:
    """
    =====================================================
    Instructor Dashboard Service

    Responsibilities
    ----------------
    • Overall classroom statistics
    • Student summaries
    • Individual student details
    • Average accuracy
    • Active learners
    • Completed learners
    =====================================================
    """

    def __init__(self, learner_profile_service):
        self.learner_profile_service = learner_profile_service

    # =====================================================
    # Dashboard Summary
    # =====================================================

    def get_dashboard(self):
        """
        Returns high-level statistics for the instructor dashboard.
        """

        profiles = self.learner_profile_service.get_all_profiles()

        total_students = len(profiles)

        active_today = 0
        completed_students = 0
        accuracy_list = []

        students = []

        for profile in profiles:

            mastery = profile.get("alphabet_mastery", {})

            completed = profile.get("completed_letters", [])

            # ------------------------------
            # Average Accuracy
            # ------------------------------

            if mastery:

                values = [
                    item.get("accuracy", 0)
                    for item in mastery.values()
                ]

                avg_accuracy = round(mean(values), 2)

            else:

                avg_accuracy = 0

            accuracy_list.append(avg_accuracy)

            # ------------------------------
            # Active Student
            # ------------------------------

            if profile.get("total_sessions", 0) > 0:
                active_today += 1

            # ------------------------------
            # Completed Student
            # ------------------------------

            if len(completed) == 26:
                completed_students += 1

            # ------------------------------
            # Student Summary
            # ------------------------------

            students.append({

                "student_id": profile.get("student_id"),

                "current_letter": profile.get(
                    "current_letter",
                    "A"
                ),

                "completed_letters": len(completed),

                "accuracy": avg_accuracy,

                "total_sessions": profile.get(
                    "total_sessions",
                    0
                ),

                "last_updated": profile.get(
    "last_updated"
)

            })

        dashboard = {

            "total_students": total_students,

            "active_students": active_today,

            "completed_students": completed_students,

            "average_accuracy": round(
                mean(accuracy_list),
                2
            ) if accuracy_list else 0,

            "students": students

        }

        return dashboard

    # =====================================================
    # Individual Student Details
    # =====================================================

    def get_student_details(self, student_id):
        """
        Returns detailed learning information for one student.
        """

        profile = self.learner_profile_service.get_profile(
            student_id
        )

        history = profile.get(
            "practice_history",
            []
        )

        mastery = profile.get(
            "alphabet_mastery",
            {}
        )

        completed = profile.get(
            "completed_letters",
            []
        )

        # ------------------------------
        # Overall Accuracy
        # ------------------------------

        if history:

            correct_count = sum(
                1
                for attempt in history
                if attempt.get("correct")
            )

            overall_accuracy = round(
                (correct_count / len(history)) * 100,
                2
            )

        else:

            overall_accuracy = 0

        # ------------------------------
        # Weak & Strong Letters
        # ------------------------------

        weak_letters = []
        strong_letters = []

        for letter, data in mastery.items():

            attempts = data.get(
                "attempts",
                0
            )

            accuracy = data.get(
                "accuracy",
                0
            )

            if attempts > 0:

                if accuracy < 60:
                    weak_letters.append(letter)

                elif accuracy >= 90 and attempts >= 3:
                    strong_letters.append(letter)

        # ------------------------------
        # Return Student Details
        # ------------------------------

        return {

            "student_id": profile.get(
                "student_id"
            ),

            "current_letter": profile.get(
                "current_letter",
                "A"
            ),

            "next_letter": profile.get(
                "next_letter",
                "A"
            ),

            "completed_letters": completed,

            "completed_count": len(
                completed
            ),

            "total_sessions": profile.get(
                "total_sessions",
                0
            ),

            "total_attempts": profile.get(
                "total_attempts",
                len(history)
            ),

            "accuracy": overall_accuracy,

            "alphabet_mastery": mastery,

            "practice_history": history,

            "strong_letters": strong_letters,

            "weak_letters": weak_letters,

            "recommendations": (
                self.learner_profile_service
                .generate_profile(student_id)
                .get("recommendations", [])
            ),

            "created_at": profile.get(
                "created_at"
            ),

            "last_updated": profile.get(
    "last_updated"
)
        }

    # =====================================================
    # Get All Profiles
    # =====================================================

    def get_all_students(self):
        """
        Returns detailed profiles for all students.
        """

        profiles = (
            self.learner_profile_service
            .get_all_profiles()
        )

        return [
            self.get_student_details(
                profile.get("student_id")
            )
            for profile in profiles
        ]