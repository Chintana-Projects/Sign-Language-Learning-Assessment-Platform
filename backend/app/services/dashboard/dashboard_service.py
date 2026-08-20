class DashboardService:

    def __init__(
        self,
        learner_profile_service,
        recommendation_engine,
        assessment_history,
        learning_state
    ):

        self.profile_service = learner_profile_service
        self.recommendation_engine = recommendation_engine
        self.assessment_history = assessment_history
        self.learning_state = learning_state

    def get_dashboard(
        self,
        student_id
    ):

        print("=" * 50)
        print("Dashboard requested for:", student_id)

        profile = self.profile_service.get_profile(student_id)
        completed_letters = profile.get(
    "completed_letters",
    []
)
        lesson_progress = {
    "completed": len(completed_letters),
    "total": 26,
    "percentage": round(
        (len(completed_letters) / 26) * 100,
        2
    )
}

        print("Loaded profile:", profile["student_id"])
        print("Completed:", profile["completed_letters"])
        print("Mastery keys:", list(profile["alphabet_mastery"].keys()))
        print("=" * 50)

        history = self.assessment_history.get_student_history(
            student_id
        )

        learning = self.learning_state.calculate(
            history
        )

        recommendations = self.recommendation_engine.generate(
            learner_profile=profile,
            confusion_pairs=self._get_confusions(profile),
            trends=[],
            learning_state=learning
        )

        # =====================================
        # Choose Next Practice
        # =====================================

        current_letter = profile.get("current_letter")
        next_practice = None
        if current_letter and current_letter != "COMPLETED":
            for recommendation in recommendations:
                recommendation_letter = (
            recommendation.get("alphabet")
            or recommendation.get("letter")
        )
                if recommendation_letter == current_letter:
                    next_practice = recommendation
                    break
        if (
    next_practice is None
    and current_letter
    and current_letter != "COMPLETED"
):
            next_practice = {

        "alphabet": current_letter,

        "reason":
            "Continue practicing the current alphabet.",

        "priority": "HIGH"

    }
        if (
    next_practice is None
    and recommendations
):
             next_practice = recommendations[0]
        return {
    "student_id": student_id,

    "profile": profile,

    "lesson_progress": lesson_progress,

    "learning_state": learning,

    "recommendations": recommendations,

    "next_practice": next_practice
}

    def _get_confusions(self, profile):

        result = []

        mastery = profile.get(
            "alphabet_mastery",
            {}
        )

        for alphabet, data in mastery.items():

            confused = data.get(
                "confused_with",
                {}
            )

            for wrong, count in confused.items():

                result.append({

                    "expected": alphabet,

                    "predicted": wrong,

                    "count": count

                })

        return result