class SignScoreCalculator:
    """
    Calculates overall gesture performance score.

    Score Components:

    1. Gesture Accuracy  -> 40%
    2. Confidence        -> 30%
    3. Gesture Stability -> 20%
    4. Timing            -> 10%

    Total Score = 100
    """

    def __init__(self):

        self.ACCURACY_WEIGHT = 40
        self.CONFIDENCE_WEIGHT = 30
        self.STABILITY_WEIGHT = 20
        self.TIMING_WEIGHT = 10

    # -------------------------------------------------
    # Calculate Overall Sign Score
    # -------------------------------------------------

    def calculate(
        self,
        correct,
        confidence,
        stability,
        time_taken
    ):

        # -------------------------------
        # Normalize confidence
        # -------------------------------

        if confidence > 1:
            confidence = confidence / 100

        confidence = max(0, min(confidence, 1))

        # -------------------------------
        # Normalize stability
        # -------------------------------

        stability = max(0, min(stability, 100))

        # -------------------------------
        # Accuracy Score
        # -------------------------------

        accuracy_score = (
            self.ACCURACY_WEIGHT
            if correct
            else 0
        )

        # -------------------------------
        # Confidence Score
        # -------------------------------

        confidence_score = (
            confidence *
            self.CONFIDENCE_WEIGHT
        )

        # -------------------------------
        # Stability Score
        # -------------------------------

        stability_score = (
            stability / 100
        ) * self.STABILITY_WEIGHT

        # -------------------------------
        # Timing Score
        # -------------------------------

        timing_score = self.calculate_timing_score(
            time_taken
        )

        # -------------------------------
        # Final Score
        # -------------------------------

        total_score = (
            accuracy_score
            + confidence_score
            + stability_score
            + timing_score
        )

        total_score = round(
            min(total_score, 100),
            2
        )

        return {

            "overall_score": total_score,

            "grade": self.get_grade(total_score),

            "components": {

                # Percentages (shown in UI)

                "accuracy": round(
                    (accuracy_score / self.ACCURACY_WEIGHT) * 100,
                    2
                ),

                "confidence": round(
                    confidence * 100,
                    2
                ),

                "stability": round(
                    stability,
                    2
                ),

                "timing": round(
                    timing_score,
                    2
                ),

                # Raw weighted scores

                "gesture_accuracy_score": round(
                    accuracy_score,
                    2
                ),

                "confidence_score": round(
                    confidence_score,
                    2
                ),

                "stability_score": round(
                    stability_score,
                    2
                ),

                "timing_score": round(
                    timing_score,
                    2
                ),

                "time_taken": round(
                    time_taken if time_taken is not None else 0,
                    2
                )
            }
        }

    # -------------------------------------------------
    # Timing Calculation
    # -------------------------------------------------

    def calculate_timing_score(
        self,
        time_taken
    ):

        if time_taken is None:
            return 0

        # Full score for <=2 sec

        if time_taken <= 2:
            return self.TIMING_WEIGHT

        # Linear decrease until 10 sec

        score = (
            self.TIMING_WEIGHT -
            ((time_taken - 2) / 8) * self.TIMING_WEIGHT
        )

        score = max(score, 0)

        return round(score, 2)

    # -------------------------------------------------
    # Performance Grade
    # -------------------------------------------------

    def get_grade(
        self,
        score
    ):

        if score >= 90:
            return "Excellent"

        elif score >= 75:
            return "Good"

        elif score >= 50:
            return "Average"

        else:
            return "Needs Improvement"