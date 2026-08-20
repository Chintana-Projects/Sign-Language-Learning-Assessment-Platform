from datetime import datetime


class ProgressAnalyzer:
    """
    Generates student progress analytics.

    Calculates:
    - Total attempts
    - Correct attempts
    - Incorrect attempts
    - Accuracy %
    - Average confidence
    - Average response time
    - Strong alphabets
    - Weak alphabets
    - Most mistaken alphabets
    - Daily practice streak
    - Improvement across attempts
    - Recent history
    """

    def __init__(self, attempts):

        self.attempts = attempts

    # -----------------------------------------
    # Total Attempts
    # -----------------------------------------

    def total_attempts(self):

        return len(self.attempts)

    # -----------------------------------------
    # Correct Attempts
    # -----------------------------------------

    def correct_attempts(self):

        return sum(
            1
            for attempt in self.attempts
            if attempt.get("correct", False)
        )

    # -----------------------------------------
    # Incorrect Attempts
    # -----------------------------------------

    def incorrect_attempts(self):

        return self.total_attempts() - self.correct_attempts()

    # -----------------------------------------
    # Accuracy Percentage
    # -----------------------------------------

    def accuracy(self):

        if not self.attempts:
            return 0

        return round(
            (
                self.correct_attempts()
                /
                self.total_attempts()
            ) * 100,
            2
        )

    # -----------------------------------------
    # Average Confidence
    # -----------------------------------------

    def average_confidence(self):

        if not self.attempts:
            return 0

        total = sum(

            attempt.get(
                "confidence",
                0
            )

            for attempt in self.attempts

        )

        return round(
            total / len(self.attempts),
            2
        )

    # -----------------------------------------
    # Average Response Time
    # -----------------------------------------

    def average_response_time(self):

        if not self.attempts:
            return 0

        total = sum(

            attempt.get(
                "inference_time_ms",
                0
            )

            for attempt in self.attempts

        )

        return round(
            total / len(self.attempts),
            2
        )

    # -----------------------------------------
    # Alphabet Performance
    # -----------------------------------------

    def alphabet_scores(self):

        scores = {}

        for attempt in self.attempts:

            letter = attempt.get(
                "expected_alphabet"
            )

            if letter is None:
                continue

            if letter not in scores:

                scores[letter] = {

                    "correct": 0,
                    "total": 0

                }

            scores[letter]["total"] += 1

            if attempt.get("correct"):

                scores[letter]["correct"] += 1

        result = {}

        for letter, data in scores.items():

            result[letter] = round(

                (
                    data["correct"]
                    /
                    data["total"]
                )
                * 100,

                2

            )

        return result

    # -----------------------------------------
    # Strongest Alphabet
    # -----------------------------------------

    def strongest_alphabet(self):

        scores = self.alphabet_scores()

        if not scores:
            return None

        return max(
            scores,
            key=scores.get
        )

    # -----------------------------------------
    # Weakest Alphabet
    # -----------------------------------------

    def weakest_alphabet(self):

        scores = self.alphabet_scores()

        if not scores:
            return None

        return min(
            scores,
            key=scores.get
        )

    # -----------------------------------------
    # Most Mistaken Alphabet
    # -----------------------------------------

    def most_mistaken(self):

        mistakes = {}

        for attempt in self.attempts:

            if not attempt.get("correct"):

                letter = attempt.get(
                    "expected_alphabet"
                )

                if letter:

                    mistakes[letter] = (

                        mistakes.get(letter, 0)

                        +

                        1

                    )

        if not mistakes:
            return None

        return max(
            mistakes,
            key=mistakes.get
        )

    # -----------------------------------------
    # Daily Practice Streak
    # -----------------------------------------

    def daily_practice_streak(self):

        if not self.attempts:
            return 0

        practice_dates = set()

        for attempt in self.attempts:

            timestamp = attempt.get(
                "timestamp"
            )

            if timestamp:

                try:

                    dt = datetime.fromisoformat(
                        timestamp
                    )

                    practice_dates.add(
                        dt.date()
                    )

                except:
                    pass

        if not practice_dates:
            return 0

        sorted_dates = sorted(
            practice_dates,
            reverse=True
        )

        streak = 1

        for i in range(
            len(sorted_dates) - 1
        ):

            difference = (
                sorted_dates[i]
                -
                sorted_dates[i + 1]
            ).days

            if difference == 1:

                streak += 1

            else:

                break

        return streak

    # -----------------------------------------
    # Total Practice Days
    # -----------------------------------------

    def total_practice_days(self):

        days = set()

        for attempt in self.attempts:

            timestamp = attempt.get(
                "timestamp"
            )

            if timestamp:

                try:

                    days.add(

                        datetime.fromisoformat(
                            timestamp
                        ).date()

                    )

                except:
                    pass

        return len(days)

    # -----------------------------------------
    # Improvement Across Attempts
    # -----------------------------------------

    def improvement(self):

        if len(self.attempts) < 2:
            return 0

        midpoint = len(self.attempts) // 2

        first_half = self.attempts[:midpoint]

        second_half = self.attempts[midpoint:]

        def calc_accuracy(records):

            if not records:
                return 0

            correct = sum(

                1

                for record in records

                if record.get("correct", False)

            )

            return (

                correct

                /

                len(records)

            ) * 100

        return round(

            calc_accuracy(second_half)

            -

            calc_accuracy(first_half),

            2

        )

    # -----------------------------------------
    # Dashboard Summary
    # -----------------------------------------

    def summary(self):

        return {

            "total_attempts":
                self.total_attempts(),

            "correct_attempts":
                self.correct_attempts(),

            "incorrect_attempts":
                self.incorrect_attempts(),

            "accuracy_percentage":
                self.accuracy(),

            "average_confidence":
                self.average_confidence(),

            "average_response_time_ms":
                self.average_response_time(),

            "strongest_alphabet":
    self.strongest_alphabet()
    if self.attempts
    else None,


"weakest_alphabet":
    self.weakest_alphabet()
    if self.attempts
    else None,

            "most_mistaken_alphabet":
                self.most_mistaken(),

            "daily_practice_streak":
                self.daily_practice_streak(),

            "total_practice_days":
                self.total_practice_days(),

            "improvement_percentage":
                self.improvement(),

            "alphabet_scores":
                self.alphabet_scores(),

            "recent_history":
                self.attempts[-10:]

        }