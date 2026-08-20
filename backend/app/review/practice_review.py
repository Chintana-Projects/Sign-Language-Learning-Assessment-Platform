from collections import Counter


class PracticeReview:
    """
    Generates complete practice review.
    """

    def __init__(self, session):

        self.session = session or {}
        self.history = self.session.get("history", [])

    # =====================================================
    # Overall Score
    # =====================================================

    def overall_score(self):
        return round(self.session.get("accuracy", 0), 2)

    # =====================================================
    # Correct Attempts
    # =====================================================

    def correct_attempts(self):

        return [
            attempt
            for attempt in self.history
            if attempt.get("correct", False)
        ]

    # =====================================================
    # Incorrect Attempts
    # =====================================================

    def incorrect_attempts(self):

        return [
            attempt
            for attempt in self.history
            if not attempt.get("correct", False)
        ]

    # =====================================================
    # Confidence Trend
    # =====================================================

    def confidence_trend(self):

        trend = []

        for index, attempt in enumerate(self.history, start=1):

            confidence = float(
                attempt.get("confidence", 0)
            )

            if confidence <= 1:
                confidence *= 100

            trend.append({

                "attempt": index,

                "expected": attempt.get("expected"),

                "predicted": attempt.get("predicted"),

                "confidence": round(confidence, 2),

                "correct": attempt.get("correct", False)

            })

        return trend

    # =====================================================
    # Feedback History
    # =====================================================

    def feedback_history(self):

        history = []

        for attempt in self.history:

            feedback = attempt.get("feedback", {})

            confidence = float(
                attempt.get("confidence", 0)
            )

            if confidence <= 1:
                confidence *= 100

            history.append({

                "expected": attempt.get("expected"),

                "predicted": attempt.get("predicted"),

                "correct": attempt.get("correct", False),

                "confidence": round(confidence, 2),

                "feedback": feedback

            })

        return history

    # =====================================================
    # Gesture Feedback Summary
    # =====================================================

    def gesture_feedback_summary(self):

        feedback_list = []

        for attempt in self.history:

            feedback = attempt.get("feedback", {})

            confidence = float(
                attempt.get("confidence", 0)
            )

            if confidence <= 1:
                confidence *= 100

            feedback_list.append({

                "expected": attempt.get("expected"),

                "predicted": attempt.get("predicted"),

                "correct": attempt.get("correct", False),

                "confidence": round(confidence, 2),

                "feedback": feedback.get(
                    "feedback_messages",
                    []
                ),

                "mistakes": feedback.get(
                    "mistakes",
                    []
                ),

                "tips": feedback.get(
                    "improvement_tips",
                    []
                )

            })

        return feedback_list

    # =====================================================
    # Common Mistakes
    # =====================================================

    def common_mistakes(self):

        mistakes = Counter()

        for attempt in self.incorrect_attempts():

            feedback = attempt.get("feedback", {})

            for mistake in feedback.get(
                    "mistakes",
                    []
            ):

                mistakes[mistake] += 1

        return dict(
            mistakes.most_common(10)
        )

    # =====================================================
    # Recommended Gestures
    # =====================================================

    def recommended_gestures(self):

        confusion = Counter()

        for attempt in self.incorrect_attempts():

            expected = attempt.get("expected")
            predicted = attempt.get("predicted")

            if (
                expected
                and
                predicted
                and
                predicted != "Unknown"
            ):

                confusion[
                    f"{expected} → {predicted}"
                ] += 1

        recommendations = []

        for pair, count in confusion.most_common(5):

            expected, predicted = pair.split(" → ")

            recommendations.append({

                "practice": expected,

                "confused_with": predicted,

                "mistakes": count,

                "reason":

                    f"You often sign '{expected}' as '{predicted}'. Practice these together."

            })

        return {

            "message":

                "Practice these gesture pairs.",

            "recommended":

                recommendations

        }

    # =====================================================
    # Session Statistics
    # =====================================================

    def session_statistics(self):

        total = len(self.history)

        correct = len(self.correct_attempts())

        incorrect = len(self.incorrect_attempts())

        if total:

            confidence = sum(

                float(h.get("confidence", 0))

                for h in self.history

            )

            if confidence <= total:
                confidence *= 100

            average_confidence = round(
                confidence / total,
                2
            )

        else:

            average_confidence = 0

        return {

            "total_attempts": total,

            "correct_attempts": correct,

            "incorrect_attempts": incorrect,

            "accuracy": self.overall_score(),

            "average_confidence": average_confidence

        }

    # =====================================================
    # Gesture Summary
    # =====================================================

    def gesture_summary(self):

        summary = {}

        for attempt in self.history:

            gesture = attempt.get("expected")

            if not gesture:
                continue

            if gesture not in summary:

                summary[gesture] = {

                    "attempts": 0,

                    "correct": 0,

                    "incorrect": 0,

                    "accuracy": 0

                }

            summary[gesture]["attempts"] += 1

            if attempt.get("correct"):

                summary[gesture]["correct"] += 1

            else:

                summary[gesture]["incorrect"] += 1

        for gesture in summary:

            attempts = summary[gesture]["attempts"]

            correct = summary[gesture]["correct"]

            summary[gesture]["accuracy"] = round(

                (correct / attempts) * 100,

                2

            )

        return summary

    # =====================================================
    # Motion Summary
    # =====================================================

    def motion_summary(self):

        if not self.history:

            return {}

        stability = []
        confidence = []
        invalid = []
        frames = []
        time = []

        for attempt in self.history:

            motion = attempt.get(
                "motion_metrics",
                {}
            )

            stability.append(
                motion.get("gesture_stability", 0)
            )

            confidence.append(
                motion.get("average_confidence", 0)
            )

            invalid.append(
                motion.get("invalid_frames", 0)
            )

            frames.append(
                motion.get("frames_analyzed", 0)
            )

            time.append(
                motion.get("time_taken", 0)
            )

        return {

            "gesture_stability":

                round(
                    sum(stability) / len(stability),
                    2
                ),

            "average_confidence":

                round(
                    sum(confidence) / len(confidence),
                    3
                ),

            "invalid_frames":

                sum(invalid),

            "frames_analyzed":

                sum(frames),

            "time_taken":

                round(
                    sum(time) / len(time),
                    2
                )

        }

    # =====================================================
    # Performance Summary
    # =====================================================

    def performance_summary(self):

        accuracy = self.overall_score()

        if accuracy >= 90:

            level = "Excellent"

            recommendation = "Excellent work!"

        elif accuracy >= 75:

            level = "Good"

            recommendation = "Practice confusing gestures."

        elif accuracy >= 50:

            level = "Average"

            recommendation = "Review mistakes."

        else:

            level = "Needs Improvement"

            recommendation = "Practice again."

        strongest = [

            g

            for g, data in self.gesture_summary().items()

            if data["accuracy"] >= 90

        ]

        return {

            "performance": level,

            "accuracy": accuracy,

            "recommendation": recommendation,

            "weakest_gestures":

                self.recommended_gestures()[
                    "recommended"
                ],

            "strongest_gestures":

                strongest

        }

    # =====================================================
    # Generate Review
    # =====================================================

    def generate_review(self):

        return {

            "overall_score":
                self.overall_score(),

            "session_statistics":
                self.session_statistics(),

            "gesture_summary":
                self.gesture_summary(),

            "gesture_feedback":
                self.gesture_feedback_summary(),

            "correct_attempts":
                self.correct_attempts(),

            "incorrect_attempts":
                self.incorrect_attempts(),

            "confidence_trend":
                self.confidence_trend(),

            "common_mistakes":
                self.common_mistakes(),

            "feedback_history":
                self.feedback_history(),

            "recommended_gestures":
                self.recommended_gestures(),

            "performance_summary":
                self.performance_summary(),

            "motion_metrics":
                self.motion_summary()

        }