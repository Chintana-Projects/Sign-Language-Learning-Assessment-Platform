
from statistics import mean


class ReportService:

    def __init__(self, assessment_history):
        self.assessment_history = assessment_history

    # ============================================================
    # STUDENT REPORT
    # ============================================================

    def get_student_report(self, student_id: str):

        # ========================================================
        # LOAD THE SAME PRACTICE HISTORY USED BY DASHBOARD
        # ========================================================

        history = self.assessment_history.get_student_history(
            student_id
        )

        if not isinstance(history, list):
            history = []

        # ========================================================
        # EMPTY REPORT
        # ========================================================

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
            if bool(
                attempt.get(
                    "correct",
                    False
                )
            )
        )

        incorrect_attempts = (
            total_attempts
            - correct_attempts
        )

        accuracy = (

            (
                correct_attempts
                /
                total_attempts
            )
            * 100

            if total_attempts > 0

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

                confidence = float(
                    confidence
                )

                # Backend may store confidence
                # either as 0-1 or 0-100.

                if confidence <= 1:
                    confidence *= 100

                # Prevent impossible values.

                confidence = max(
                    0,
                    min(
                        confidence,
                        100
                    )
                )

                confidences.append(
                    confidence
                )

            except (
                TypeError,
                ValueError
            ):
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

            if not isinstance(
                sign_score,
                dict
            ):
                continue

            score = sign_score.get(
                "overall_score"
            )

            try:

                if score is not None:

                    scores.append(
                        float(score)
                    )

            except (
                TypeError,
                ValueError
            ):
                continue

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

            if not expected:
                continue

            expected = str(
                expected
            ).upper().strip()

            # Only A-Z count as alphabet letters.

            if len(expected) == 1 and expected.isalpha():

                letters.add(
                    expected
                )

        # Always return alphabetical order.

        letters_practiced = sorted(
            letters
        )

        # ========================================================
        # LETTER STATISTICS
        # ========================================================

        letter_stats = {}

        for attempt in history:

            expected = attempt.get(
                "expected"
            )

            if not expected:
                continue

            expected = str(
                expected
            ).upper().strip()

            if len(expected) != 1:
                continue

            if not expected.isalpha():
                continue

            if expected not in letter_stats:

                letter_stats[expected] = {

                    "attempts": 0,

                    "correct": 0,

                    "incorrect": 0

                }

            letter_stats[
                expected
            ]["attempts"] += 1

            if bool(
                attempt.get(
                    "correct",
                    False
                )
            ):

                letter_stats[
                    expected
                ]["correct"] += 1

            else:

                letter_stats[
                    expected
                ]["incorrect"] += 1

        # ========================================================
        # WEAK LETTERS
        # ========================================================

        weak_letters = []

        for letter, stats in letter_stats.items():

            attempts = stats[
                "attempts"
            ]

            correct = stats[
                "correct"
            ]

            letter_accuracy = (

                (
                    correct
                    /
                    attempts
                )
                * 100

                if attempts > 0

                else 0
            )

            # Below 70% = weak.

            if letter_accuracy < 70:

                weak_letters.append({

                    "letter":
                        letter,

                    "attempts":
                        attempts,

                    "correct":
                        correct,

                    "incorrect":
                        stats[
                            "incorrect"
                        ],

                    "accuracy":
                        round(
                            letter_accuracy,
                            2
                        )

                })

        weak_letters.sort(
            key=lambda item:
                item["accuracy"]
        )

        # ========================================================
        # RECENT ATTEMPTS
        # ========================================================

        recent_history = sorted(

            history,

            key=lambda attempt: (

                attempt.get(
                    "timestamp"
                )
                or
                attempt.get(
                    "saved_at"
                )
                or
                ""

            ),

            reverse=True

        )[:10]

        recent_attempts = []

        for attempt in recent_history:

            confidence = attempt.get(
                "confidence",
                0
            )

            try:

                confidence = float(
                    confidence
                )

                if confidence <= 1:

                    confidence *= 100

                confidence = max(
                    0,
                    min(
                        confidence,
                        100
                    )
                )

            except (
                TypeError,
                ValueError
            ):

                confidence = 0

            sign_score = attempt.get(
                "sign_score",
                {}
            )

            if isinstance(
                sign_score,
                dict
            ):

                score = sign_score.get(
                    "overall_score",
                    0
                )

            else:

                score = 0

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
                        confidence / 100,
                        3
                    ),

                "correct":
                    bool(
                        attempt.get(
                            "correct",
                            False
                        )
                    ),

                "score":
                    score,

                "timestamp":
                    attempt.get(
                        "timestamp"
                    )
                    or
                    attempt.get(
                        "saved_at"
                    )

            })

        # ========================================================
        # FINAL REPORT
        # ========================================================

        return {

            "success":
                True,

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
                    )

            },

            "letters_practiced":
                letters_practiced,

            "weak_letters":
                weak_letters,

            "recent_attempts":
                recent_attempts

        }

