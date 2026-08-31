from datetime import datetime, timedelta


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

    # =========================================================
    # DASHBOARD
    # =========================================================

    def get_dashboard(self, student_id):

        print("=" * 50)
        print("Dashboard requested for:", student_id)

        # =====================================================
        # LOAD PROFILE
        # =====================================================

        profile = self.profile_service.get_profile(
            student_id
        )

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

        print(
            "Loaded profile:",
            profile.get("student_id")
        )

        print(
            "Completed:",
            completed_letters
        )

        print(
            "Mastery keys:",
            list(
                profile.get(
                    "alphabet_mastery",
                    {}
                ).keys()
            )
        )

        # =====================================================
        # LOAD STUDENT HISTORY
        # =====================================================

        history = self.assessment_history.get_student_history(
            student_id
        )

        print(
            "History records:",
            len(history)
        )

        # =====================================================
        # LEARNING STATE
        # =====================================================

        learning = self.learning_state.calculate(
            history
        )

        # =====================================================
        # RECOMMENDATIONS
        # =====================================================

        recommendations = (
            self.recommendation_engine.generate(
                learner_profile=profile,
                confusion_pairs=self._get_confusions(
                    profile
                ),
                trends=[],
                learning_state=learning
            )
        )

        # =====================================================
        # RECENT PRACTICE
        # =====================================================

        recent_practice = self._get_recent_practice(
            history
        )

        # =====================================================
        # WEEKLY ACTIVITY
        # =====================================================

        weekly_activity = self._get_weekly_activity(
            history
        )

        # =====================================================
        # NEXT PRACTICE
        # =====================================================

        current_letter = profile.get(
            "current_letter"
        )

        next_practice = None

        if (
            current_letter
            and current_letter != "COMPLETED"
        ):

            for recommendation in recommendations:

                recommendation_letter = (
                    recommendation.get("alphabet")
                    or recommendation.get("letter")
                )

                if (
                    recommendation_letter
                    == current_letter
                ):

                    next_practice = recommendation

                    break

        # =====================================================
        # FALLBACK CURRENT LETTER
        # =====================================================

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

        # =====================================================
        # FALLBACK RECOMMENDATION
        # =====================================================

        if (
            next_practice is None
            and recommendations
        ):

            next_practice = recommendations[0]

        print(
            "Recent practice:",
            len(recent_practice)
        )

        print(
            "Weekly activity:",
            weekly_activity
        )

        print("=" * 50)

        # =====================================================
        # DASHBOARD RESPONSE
        # =====================================================

        return {

            "student_id": student_id,

            "profile": profile,

            "lesson_progress": lesson_progress,

            "learning_state": learning,

            "recommendations": recommendations,

            "next_practice": next_practice,

            "history": history,

            "recent_practice": recent_practice,

            "weekly_activity": weekly_activity

        }

    # =========================================================
    # RECENT PRACTICE
    # =========================================================

    def _get_recent_practice(
        self,
        history
    ):

        if not history:
            return []

        # -----------------------------------------------------
        # Sort newest first
        # -----------------------------------------------------

        sorted_history = sorted(
            history,
            key=lambda x: (
                x.get("timestamp")
                or x.get("saved_at")
                or ""
            ),
            reverse=True
        )

        # -----------------------------------------------------
        # Keep latest 10 attempts
        # -----------------------------------------------------

        recent = sorted_history[:10]

        result = []

        for attempt in recent:

            # -------------------------------------------------
            # Confidence
            # -------------------------------------------------

            confidence = attempt.get(
                "confidence",
                0
            )

            try:

                confidence = float(
                    confidence
                )

            except (
                TypeError,
                ValueError
            ):

                confidence = 0

            # -------------------------------------------------
            # Backend normally stores confidence as 0-1
            # Convert to percentage
            # -------------------------------------------------

            if confidence <= 1:

                confidence *= 100

            # -------------------------------------------------
            # Add recent attempt
            # -------------------------------------------------

            result.append({

                "expected":
                    attempt.get(
                        "expected"
                    ),

                "predicted":
                    attempt.get(
                        "predicted"
                    ),

                "confidence":
                    round(
                        confidence,
                        2
                    ),

                "correct":
                    bool(
                        attempt.get(
                            "correct"
                        )
                    ),

                "timestamp":
                    attempt.get(
                        "timestamp"
                    )
                    or attempt.get(
                        "saved_at"
                    ),

                "sign_score":
                    attempt.get(
                        "sign_score",
                        0
                    )

            })

        return result

    # =========================================================
    # WEEKLY ACTIVITY
    # =========================================================

    def _get_weekly_activity(
        self,
        history
    ):

        today = datetime.now().date()

        activity = {}

        # -----------------------------------------------------
        # Create the last 7 days
        # -----------------------------------------------------

        for i in range(
            6,
            -1,
            -1
        ):

            day = (
                today
                - timedelta(days=i)
            )

            key = day.isoformat()

            activity[key] = {

                "date": key,

                "attempts": 0,

                "correct": 0,

                "accuracy": 0

            }

        # -----------------------------------------------------
        # Process saved attempts
        # -----------------------------------------------------

        for attempt in history:

            timestamp = attempt.get(
                "timestamp"
            )

            if not timestamp:

                timestamp = attempt.get(
                    "saved_at"
                )

            if not timestamp:
                continue

            try:

                # -------------------------------------------------
                # Handle ISO timestamps
                # -------------------------------------------------

                timestamp_clean = (
                    str(timestamp)
                    .replace(
                        "Z",
                        ""
                    )
                )

                attempt_datetime = (
                    datetime.fromisoformat(
                        timestamp_clean
                    )
                )

                attempt_date = (
                    attempt_datetime.date()
                )

            except (
                ValueError,
                TypeError
            ):

                continue

            key = attempt_date.isoformat()

            # -------------------------------------------------
            # Only include last 7 days
            # -------------------------------------------------

            if key not in activity:
                continue

            activity[key]["attempts"] += 1

            # -------------------------------------------------
            # Correct attempt
            # -------------------------------------------------

            if attempt.get(
                "correct"
            ):

                activity[key]["correct"] += 1

        # -----------------------------------------------------
        # Calculate daily accuracy
        # -----------------------------------------------------

        for day in activity.values():

            attempts = day["attempts"]

            correct = day["correct"]

            if attempts > 0:

                day["accuracy"] = round(
                    (
                        correct
                        / attempts
                    ) * 100,
                    2
                )

            else:

                day["accuracy"] = 0

        # -----------------------------------------------------
        # Return chronological order
        # -----------------------------------------------------

        return list(
            activity.values()
        )

    # =========================================================
    # CONFUSION ANALYSIS
    # =========================================================

    def _get_confusions(
        self,
        profile
    ):

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

                    "expected":
                        alphabet,

                    "predicted":
                        wrong,

                    "count":
                        count

                })

        return result