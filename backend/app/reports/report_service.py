from statistics import mean


class ReportService:

    def __init__(self, assessment_history):
        self.assessment_history = assessment_history

    # ============================================================
    # STUDENT REPORT
    # ============================================================

    def get_student_report(self, student_id: str):

        history = self.assessment_history.get_student_history(
            student_id
        )

        if not history:
            return {
                "success": True,
                "student_id": student_id,
                "summary": {
                    "total_attempts": 0,
                    "correct_attempts": 0,
                    "incorrect_attempts": 0,
                    "accuracy": 0,
                    "average_confidence": 0,
                    "average_score": 0,
                },
                "letters_practiced": [],
                "weak_letters": [],
                "recent_attempts": [],
            }

        # ========================================================
        # BASIC COUNTS
        # ========================================================

        total_attempts = len(history)

        correct_attempts = sum(
            1
            for attempt in history
            if attempt.get("correct", False)
        )

        incorrect_attempts = (
            total_attempts - correct_attempts
        )

        accuracy = (
            (correct_attempts / total_attempts) * 100
            if total_attempts
            else 0
        )

        # ========================================================
        # CONFIDENCE
        # ========================================================

        confidences = []

        for attempt in history:

            confidence = attempt.get(
                "confidence",
                0
            )

            try:
                confidence = float(confidence)

                if confidence <= 1:
                    confidence *= 100

                confidences.append(confidence)

            except (TypeError, ValueError):
                continue

        average_confidence = (
            mean(confidences)
            if confidences
            else 0
        )

        # ========================================================
        # SIGN SCORE
        # ========================================================

        scores = []

        for attempt in history:

            sign_score = attempt.get(
                "sign_score",
                {}
            )

            if isinstance(sign_score, dict):

                score = sign_score.get(
                    "overall_score"
                )

                try:
                    if score is not None:
                        scores.append(float(score))
                except (TypeError, ValueError):
                    pass

        average_score = (
            mean(scores)
            if scores
            else 0
        )

        # ========================================================
        # LETTERS PRACTICED
        # ========================================================

        letters = set()

        for attempt in history:

            expected = attempt.get(
                "expected"
            )

            if expected:
                letters.add(
                    str(expected).upper()
                )

        letters_practiced = sorted(
            letters
        )

        # ========================================================
        # WEAK / CONFUSED LETTERS
        # ========================================================

        letter_stats = {}

        for attempt in history:

            expected = str(
                attempt.get(
                    "expected",
                    ""
                )
            ).upper()

            if not expected:
                continue

            if expected not in letter_stats:

                letter_stats[expected] = {
                    "attempts": 0,
                    "correct": 0,
                    "incorrect": 0,
                }

            letter_stats[expected]["attempts"] += 1

            if attempt.get(
                "correct",
                False
            ):
                letter_stats[expected]["correct"] += 1
            else:
                letter_stats[expected]["incorrect"] += 1

        weak_letters = []

        for letter, stats in letter_stats.items():

            attempts = stats["attempts"]

            letter_accuracy = (
                (stats["correct"] / attempts) * 100
                if attempts
                else 0
            )

            # Consider a letter weak when
            # accuracy is below 70%.
            if letter_accuracy < 70:

                weak_letters.append({
                    "letter": letter,
                    "attempts": attempts,
                    "correct": stats["correct"],
                    "incorrect": stats["incorrect"],
                    "accuracy": round(
                        letter_accuracy,
                        2
                    ),
                })

        weak_letters.sort(
            key=lambda item: item["accuracy"]
        )

        # ========================================================
        # RECENT ATTEMPTS
        # ========================================================

        recent_history = history[-10:]

        recent_attempts = []

        for attempt in recent_history:

            recent_attempts.append({

                "assessment_id":
                    attempt.get(
                        "assessment_id"
                    ),

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
                        float(
                            attempt.get(
                                "confidence",
                                0
                            )
                        ),
                        3
                    ),

                "correct":
                    attempt.get(
                        "correct",
                        False
                    ),

                "score":
                    attempt.get(
                        "sign_score",
                        {}
                    ).get(
                        "overall_score",
                        0
                    )
                    if isinstance(
                        attempt.get(
                            "sign_score",
                            {}
                        ),
                        dict
                    )
                    else 0,

                "timestamp":
                    attempt.get(
                        "timestamp"
                    ),
            })

        # ========================================================
        # FINAL REPORT
        # ========================================================

        return {

            "success": True,

            "student_id":
                student_id,

            "summary": {

                "total_attempts":
                    total_attempts,

                "correct_attempts":
                    correct_attempts,

                "incorrect_attempts":
                    incorrect_attempts,

                "accuracy":
                    round(
                        accuracy,
                        2
                    ),

                "average_confidence":
                    round(
                        average_confidence,
                        2
                    ),

                "average_score":
                    round(
                        average_score,
                        2
                    ),
            },

            "letters_practiced":
                letters_practiced,

            "weak_letters":
                weak_letters,

            "recent_attempts":
                recent_attempts,
        }