from collections import defaultdict


class ConfidenceAnalyzer:

    def analyze(self, attempts):

        confidence_data = defaultdict(list)

        # =====================================
        # Collect confidence per gesture
        # =====================================

        for attempt in attempts:

            gesture = attempt.get("expected")
            confidence = attempt.get("confidence", 0)

            if gesture is None:
                continue

            try:
                confidence = float(confidence)
            except (TypeError, ValueError):
                confidence = 0

            # Normalize if stored as percentage (e.g. 85 instead of 0.85)
            if confidence > 1:
                confidence = confidence / 100

            confidence_data[gesture].append(confidence * 100)

        # =====================================
        # Calculate average confidence
        # =====================================

        results = []

        for gesture, values in confidence_data.items():

            average = sum(values) / len(values)

            if average < 50:
                priority = "HIGH"
            elif average < 70:
                priority = "MEDIUM"
            else:
                priority = "LOW"

            results.append({
                "gesture": gesture,
                "average_confidence": round(average, 2),
                "attempts": len(values),
                "priority": priority
            })

        # Lowest confidence first
        results.sort(key=lambda x: x["average_confidence"])

        return results