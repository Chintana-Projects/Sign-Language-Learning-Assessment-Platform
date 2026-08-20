class LearningState:

    def calculate(
        self,
        attempts
    ):

        # =====================================
        # No Attempts
        # =====================================

        if not attempts:

            return {

                "level": "Beginner",

                "message": "Start practicing gestures.",

                "next_goal": "Complete 5 practice attempts.",

                "progress": 0,

                "metrics": {

                    "attempts": 0,

                    "accuracy": 0,

                    "confidence": 0,

                    "stability": 0

                }

            }

        total = len(attempts)

        # =====================================
        # Accuracy
        # =====================================

        correct = sum(

            1

            for a in attempts

            if a.get(
                "correct",
                False
            )

        )

        accuracy = (

            correct / total

        ) * 100

        # =====================================
        # Confidence
        # =====================================

        confidence_values = []

        for a in attempts:

            confidence = a.get(
                "confidence",
                0
            )

            try:
                confidence = float(confidence)
            except (TypeError, ValueError):
                confidence = 0

            if confidence <= 1:
                confidence *= 100

            confidence_values.append(confidence)

        average_confidence = (

            sum(confidence_values)

            /

            len(confidence_values)

        )

        # =====================================
        # Stability
        # =====================================

        stability_values = []

        for a in attempts:

            motion = a.get(
                "motion_metrics",
                {}
            )

            stability = motion.get(
                "gesture_stability",
                0
            )

            try:
                stability = float(stability)
            except (TypeError, ValueError):
                stability = 0

            stability_values.append(stability)

        average_stability = (

            sum(stability_values)

            /

            len(stability_values)

        )

        # =====================================
        # Progress Score
        # =====================================

        progress = round(

            (

                accuracy * 0.5 +

                average_confidence * 0.3 +

                average_stability * 0.2

            ),

            2

        )

        # =====================================
        # Mastered
        # =====================================

        if (

            total >= 10

            and accuracy >= 90

            and average_confidence >= 75

            and average_stability >= 70

        ):

            level = "Mastered"

            message = "Excellent control. Maintain consistency."

            next_goal = "Practice new alphabets."

        # =====================================
        # Advanced
        # =====================================

        elif (

            total >= 8

            and accuracy >= 85

            and average_confidence >= 65

        ):

            level = "Advanced"

            message = "Very good performance. Almost mastered."

            next_goal = "Improve stability."

        # =====================================
        # Good
        # =====================================

        elif (

            total >= 5

            and accuracy >= 80

            and average_confidence >= 50

        ):

            level = "Good"

            message = "Gesture is improving. Continue practicing."

            next_goal = "Increase confidence."

        # =====================================
        # Improving
        # =====================================

        elif accuracy >= 40:

            level = "Improving"

            message = "Keep practicing this gesture."

            next_goal = "Improve accuracy above 80%."

        # =====================================
        # Beginner
        # =====================================

        else:

            level = "Beginner"

            message = "Needs more practice."

            next_goal = "Focus on correct hand positioning."

        # =====================================
        # Return
        # =====================================

        return {

            "level": level,

            "message": message,

            "next_goal": next_goal,

            "progress": progress,

            "metrics": {

                "attempts": total,

                "accuracy": round(
                    accuracy,
                    2
                ),

                "confidence": round(
                    average_confidence,
                    2
                ),

                "stability": round(
                    average_stability,
                    2
                )

            }

        }