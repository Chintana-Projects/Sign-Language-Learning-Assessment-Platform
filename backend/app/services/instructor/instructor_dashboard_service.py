from statistics import mean

from app.database.database import SessionLocal
from app.models.user_model import User
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
    • Skill development analytics
    =====================================================
    """

    def __init__(self, learner_profile_service):
        self.learner_profile_service = learner_profile_service

    # =====================================================
    # Dashboard Summary
    # =====================================================

    def get_dashboard(self):
        """
        Returns high-level statistics for the instructor dashboard
        including learner skill development information.
        """

        profiles = (
            self.learner_profile_service
            .get_all_profiles()
        )

        total_students = len(profiles)

        active_students = 0
        completed_students = 0
        certified_students = 0

        accuracy_list = []
        students = []
        beginner_count = 0
        intermediate_count = 0
        advanced_count = 0
        professional_count = 0
        total_completed_letters = 0
        total_possible_letters = total_students * 26

        letter_data = {}

        for profile in profiles:

            mastery = profile.get(
                "alphabet_mastery",
                {}
            )

            completed = profile.get(
                "completed_letters",
                []
            )

            history = profile.get(
                "practice_history",
                []
            )

            # -------------------------------------------------
            # Average Accuracy
            # -------------------------------------------------

            overall_accuracy = profile.get(
                "overall_accuracy"
            )

            if overall_accuracy is not None:
                avg_accuracy = round(
                    float(overall_accuracy),
                    2
                )
            elif mastery:
                values = [
                    float(item.get("accuracy", 0))
                    for item in mastery.values()
                    if isinstance(item, dict)
                ]
                avg_accuracy = (
                    round(mean(values), 2)
                    if values
                    else 0
                )
            else:
                avg_accuracy = 0

            # Executed for ALL students regardless of branch
            accuracy_list.append(avg_accuracy)

            # -------------------------------------------------
            # Active Student
            # -------------------------------------------------

            if profile.get(
                "total_sessions",
                0
            ) > 0:

                active_students += 1

            # -------------------------------------------------
            # Completed Student
            # -------------------------------------------------

            if len(completed) >= 26:

                completed_students += 1
                print(
    profile.get("student_id"),
    profile.get("certified")
)
                

            if profile.get("certified", False):
                print("ADDING CERTIFIED")
                certified_students += 1
            level = profile.get(
    "certification_level",
    "Beginner"
)
            if level == "Beginner":
                beginner_count += 1
            elif level == "Intermediate":
                intermediate_count += 1
            elif level == "Advanced":
                advanced_count += 1
            elif level == "Professional":
                professional_count += 1
                

            # -------------------------------------------------
            # Completed Letters
            # -------------------------------------------------

            total_completed_letters += len(completed)

            # -------------------------------------------------
            # Letter Skill Development
            # -------------------------------------------------

            for letter, data in mastery.items():

                if not isinstance(data, dict):
                    continue

                attempts = int(
                    data.get(
                        "attempts",
                        0
                    )
                )

                accuracy = float(
                    data.get(
                        "accuracy",
                        0
                    )
                )

                if letter not in letter_data:

                    letter_data[letter] = {
                        "attempts": 0,
                        "accuracy_total": 0,
                        "students": 0
                    }

                letter_data[letter]["attempts"] += attempts

                letter_data[letter]["accuracy_total"] += accuracy

                if attempts > 0:

                    letter_data[letter]["students"] += 1

            # -------------------------------------------------
            # Student Summary
            # -------------------------------------------------

            student_id = profile.get("student_id")
            student_name = student_id
            try:
                db = SessionLocal()
                user = db.query(User).filter(
        User.id == int(student_id)
    ).first()
                if user:
                    student_name = user.full_name
            except Exception:
                pass
            finally:
                try:
                    db.close()
                except:
                    pass
            students.append({

    "student_id": student_id,

    "student_name": student_name,
    

                "current_letter": profile.get(
                    "current_letter",
                    "A"
                ),

                "completed_letters": len(
                    completed
                ),

                "accuracy": round(avg_accuracy, 2),

                "total_sessions": profile.get(
                    "total_sessions",
                    0
                ),

                "total_attempts": profile.get(
                    "total_attempts",
                    len(history)
                ),

                "alphabet_mastery": mastery,

                "practice_history": history,

                "last_updated": profile.get(
                    "last_updated"
                )

            })

        # =====================================================
        # Overall Class Accuracy
        # =====================================================

        average_accuracy = (
            round(
                mean(accuracy_list),
                2
            )
            if accuracy_list
            else 0
        )

        # =====================================================
        # Overall Skill Progress
        # =====================================================

        overall_progress = (
            round(
                (
                    total_completed_letters /
                    total_possible_letters
                ) * 100,
                2
            )
            if total_possible_letters > 0
            else 0
        )

        # =====================================================
        # Letter Skill Development
        # =====================================================

        letter_performance = []

        for letter, data in letter_data.items():

            attempts = data["attempts"]
            students_count = data["students"]

            accuracy = (
                round(
                    data["accuracy_total"] /
                    students_count,
                    2
                )
                if students_count > 0
                else 0
            )

            letter_performance.append({

                "letter": letter,

                "attempts": attempts,

                "accuracy": accuracy,

                "students": students_count

            })

        # -----------------------------------------------------
        # Sort by accuracy
        # -----------------------------------------------------

        strongest_letters = sorted(
            letter_performance,
            key=lambda item: item["accuracy"],
            reverse=True
        )[:5]

        weakest_letters = sorted(
            letter_performance,
            key=lambda item: item["accuracy"]
        )[:5]

        # -----------------------------------------------------
        # Sort overall letter activity
        # -----------------------------------------------------

        letter_performance.sort(
            key=lambda item: item["attempts"],
            reverse=True
        )

        # =====================================================
        # Skill Development Response
        # =====================================================

        skill_development = {

            "overall_progress": overall_progress,

            "strongest_letters": strongest_letters,

            "weakest_letters": weakest_letters,

            "letter_performance": letter_performance

        }
        print(
            "CERTIFIED COUNT:",
            certified_students
        )

        # =====================================================
        # Dashboard Response
        # =====================================================

        return {

    "total_students": total_students,

    "active_students": active_students,

    "certified_students": certified_students,

    "completed_students": completed_students,

    "average_accuracy": average_accuracy,

    "beginner_students": beginner_count,

    "intermediate_students": intermediate_count,

    "advanced_students": advanced_count,

    "professional_students": professional_count,

    "students": students,

    "skill_development": skill_development

}

    # =====================================================
    # Individual Student Details
    # =====================================================

    def get_student_details(self, student_id):
        """
        Returns detailed learning information
        for one student.
        """

        profile = (
            self.learner_profile_service
            .get_profile(student_id)
        )

        # -------------------------------------------------
        # Safety Check
        # -------------------------------------------------

        if not profile:

            raise ValueError(
                "Student profile not found."
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

        # -------------------------------------------------
        # Overall Accuracy
        # -------------------------------------------------

        overall_accuracy = profile.get(
            "overall_accuracy",
            0
        )

        if history:

            correct_count = sum(
                1
                for attempt in history
                if attempt.get("correct") is True
            )

            overall_accuracy = round(
                (correct_count / len(history)) * 100,
                2
            )

        # -------------------------------------------------
        # Weak & Strong Letters
        # -------------------------------------------------

        weak_letters = []
        strong_letters = []

        for letter, data in mastery.items():

            if not isinstance(data, dict):
                continue

            attempts = int(
                data.get(
                    "attempts",
                    0
                )
            )

            accuracy = float(
                data.get(
                    "accuracy",
                    0
                )
            )

            if attempts <= 0:
                continue

            # Weak letter
            if accuracy < 60:

                weak_letters.append(letter)

            # Strong letter
            elif (
                accuracy >= 90
                and attempts >= 3
            ):

                strong_letters.append(letter)

        # -------------------------------------------------
        # Recommendations
        # -------------------------------------------------

        try:

            generated_profile = (
                self.learner_profile_service
                .generate_profile(student_id)
            )

            recommendations = (
                generated_profile.get(
                    "recommendations",
                    []
                )
                if generated_profile
                else []
            )

        except Exception:

            recommendations = []

        # -------------------------------------------------
        # Student Details Response
        # -------------------------------------------------

        return {

            "student_id": profile.get(
                "student_id",
                student_id
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

            "recommendations": recommendations,

            "created_at": profile.get(
                "created_at"
            ),

            "last_updated": profile.get(
                "last_updated"
            )

        }

    # =====================================================
    # Get All Students
    # =====================================================

    def get_all_students(self):
        """
        Returns detailed profiles for all students.
        """

        profiles = (
            self.learner_profile_service
            .get_all_profiles()
        )

        students = []

        for profile in profiles:

            student_id = profile.get(
                "student_id"
            )

            if not student_id:
                continue

            students.append(
                self.get_student_details(
                    student_id
                )
            )

        return students