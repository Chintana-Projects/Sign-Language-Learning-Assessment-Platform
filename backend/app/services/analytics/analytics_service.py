from collections import Counter
from datetime import datetime, timedelta


class AnalyticsService:
    """
    Generates student progress analytics.

    Tracks:
    - Total attempts
    - Accuracy
    - Average confidence
    - Strongest alphabets
    - Weakest alphabets
    - Most mistaken alphabets
    - Daily streak
    - Recent history
    """

    def generate_dashboard(self, attempts):

        if not attempts:

            return {
                "total_attempts": 0,
                "accuracy_percentage": 0,
                "average_confidence": 0,
                "strongest_alphabet": None,
                "weakest_alphabet": None,
                "most_mistaken_alphabet": None,
                "daily_practice_streak": 0,
                "recent_history": []
            }


        total_attempts = len(attempts)


        # -----------------------------
        # Accuracy
        # -----------------------------

        correct_count = sum(
            1 for a in attempts
            if a["correct"]
        )


        accuracy = round(
            (correct_count / total_attempts) * 100,
            2
        )


        # -----------------------------
        # Average Confidence
        # -----------------------------

        avg_confidence = round(

            sum(
                a["confidence"]
                for a in attempts
            )
            /
            total_attempts,

            2
        )


        # -----------------------------
        # Alphabet Performance
        # -----------------------------

        alphabet_stats = {}


        for attempt in attempts:

            letter = attempt["expected"]

            if letter not in alphabet_stats:

                alphabet_stats[letter] = {
                    "correct": 0,
                    "total": 0
                }


            alphabet_stats[letter]["total"] += 1


            if attempt["correct"]:

                alphabet_stats[letter]["correct"] += 1



        alphabet_accuracy = {}


        for letter, data in alphabet_stats.items():

            alphabet_accuracy[letter] = round(
                (
                    data["correct"]
                    /
                    data["total"]
                )
                *
                100,

                2
            )


        strongest = max(
            alphabet_accuracy,
            key=alphabet_accuracy.get
        )


        weakest = min(
            alphabet_accuracy,
            key=alphabet_accuracy.get
        )



        # -----------------------------
        # Most Mistaken Alphabet
        # -----------------------------

        mistakes = Counter()


        for attempt in attempts:

            if not attempt["correct"]:

                mistakes[
                    attempt["expected"]
                ] += 1



        most_mistaken = (

            mistakes.most_common(1)[0][0]

            if mistakes

            else None
        )



        # -----------------------------
        # Daily Practice Streak
        # -----------------------------

        streak = self.calculate_streak(
            attempts
        )



        return {

            "total_attempts":
                total_attempts,

            "accuracy_percentage":
                accuracy,

            "average_confidence":
                avg_confidence,

            "strongest_alphabet":
                strongest,

            "weakest_alphabet":
                weakest,

            "most_mistaken_alphabet":
                most_mistaken,

            "daily_practice_streak":
                streak,

            "recent_history":
                attempts[-10:]

        }



    # -----------------------------------------
    # Daily streak calculation
    # -----------------------------------------

    def calculate_streak(self, attempts):

        if not attempts:

            return 0


        dates = set()


        for attempt in attempts:

            date = (
                attempt["timestamp"]
                .split("T")[0]
            )

            dates.add(date)



        today = datetime.now().date()


        streak = 0


        while str(
            today - timedelta(days=streak)
        ) in dates:

            streak += 1



        return streak