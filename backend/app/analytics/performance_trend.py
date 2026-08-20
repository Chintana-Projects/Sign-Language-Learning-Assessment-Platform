from collections import defaultdict


class PerformanceTrendAnalyzer:

    def analyze(
        self,
        attempts
    ):

        gestures = defaultdict(list)

        # =====================================
        # Group attempts by alphabet
        # =====================================

        for attempt in attempts:

            gesture = attempt.get("expected")

            if gesture:
                gestures[gesture].append(attempt)

        results = []

        # =====================================
        # Calculate trends
        # =====================================

        for gesture, data in gestures.items():

            # Need minimum attempts
            # for reliable trend
            if len(data) < 4:
                continue

            split = len(data) // 2

            previous_attempts = data[:split]
            recent_attempts = data[split:]

            # -------------------------------
            # Accuracy Trend
            # -------------------------------

            previous_accuracy = self.calculate_accuracy(
                previous_attempts
            )

            recent_accuracy = self.calculate_accuracy(
                recent_attempts
            )

            accuracy_difference = (
                recent_accuracy -
                previous_accuracy
            )

            accuracy_trend = self.get_trend(
                accuracy_difference
            )

            # -------------------------------
            # Confidence Trend
            # -------------------------------

            previous_confidence = self.calculate_confidence(
                previous_attempts
            )

            recent_confidence = self.calculate_confidence(
                recent_attempts
            )

            confidence_difference = (
                recent_confidence -
                previous_confidence
            )

            confidence_trend = self.get_trend(
                confidence_difference
            )

            # -------------------------------
            # Stability Trend
            # -------------------------------

            previous_stability = self.calculate_stability(
                previous_attempts
            )

            recent_stability = self.calculate_stability(
                recent_attempts
            )

            stability_difference = (
                recent_stability -
                previous_stability
            )

            stability_trend = self.get_trend(
                stability_difference
            )

            results.append({

                "gesture": gesture,

                "total_attempts": len(data),

                # Accuracy

                "previous_accuracy": round(
                    previous_accuracy,
                    2
                ),

                "recent_accuracy": round(
                    recent_accuracy,
                    2
                ),

                "accuracy_difference": round(
                    accuracy_difference,
                    2
                ),

                "accuracy_trend": accuracy_trend,

                # Confidence

                "previous_confidence": round(
                    previous_confidence,
                    2
                ),

                "recent_confidence": round(
                    recent_confidence,
                    2
                ),

                "confidence_difference": round(
                    confidence_difference,
                    2
                ),

                "confidence_trend": confidence_trend,

                # Stability

                "previous_stability": round(
                    previous_stability,
                    2
                ),

                "recent_stability": round(
                    recent_stability,
                    2
                ),

                "stability_difference": round(
                    stability_difference,
                    2
                ),

                "stability_trend": stability_trend,

                # Overall learning trend

                "overall_trend": self.overall_trend(
                    accuracy_trend,
                    confidence_trend,
                    stability_trend
                )

            })

        return results

    # =====================================
    # Trend Calculator
    # =====================================

    def get_trend(
        self,
        difference
    ):

        if difference >= 10:
            return "IMPROVING"

        elif difference <= -10:
            return "DECLINING"

        return "STABLE"

    # =====================================
    # Accuracy Calculator
    # =====================================

    def calculate_accuracy(
        self,
        attempts
    ):

        if not attempts:
            return 0

        correct = sum(
            1
            for item in attempts
            if item.get(
                "correct",
                False
            )
        )

        return (
            correct /
            len(attempts)
        ) * 100
        # =====================================
    # Confidence Calculator
    # =====================================

    def calculate_confidence(
        self,
        attempts
    ):

        if not attempts:
            return 0

        values = []

        for item in attempts:

            confidence = item.get(
    "confidence"
            )
            if confidence is None:
                confidence = item.get(
        "motion_metrics",
        {}
    ).get(
        "average_confidence",
        0
    )

            # Handle None/string values safely
            try:
                confidence = float(confidence)
            except (TypeError, ValueError):
                confidence = 0

            # Normalize if stored as 0-1
            if confidence <= 1:
                confidence *= 100

            values.append(confidence)

        return (
            sum(values)
            /
            len(values)
        )

 
    def calculate_stability(
    self,
    attempts
):
        if not attempts:
            return 0
        values = []
        for item in attempts:
            motion = item.get(
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

        values.append(stability)
        return (
        sum(values)
        /
        len(values)
    )
    # =====================================
    # Overall Trend
    # =====================================

    def overall_trend(
        self,
        accuracy,
        confidence,
        stability
    ):

        trends = [
            accuracy,
            confidence,
            stability
        ]

        improving = trends.count("IMPROVING")
        declining = trends.count("DECLINING")

        if improving >= 2:
            return "IMPROVING"

        if declining >= 2:
            return "DECLINING"

        return "STABLE"