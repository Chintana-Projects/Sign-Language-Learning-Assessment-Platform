from datetime import datetime


class AttemptTracker:
    """
    Stores every learning attempt.

    Tracks:
    - Student ID
    - Expected alphabet
    - Predicted alphabet
    - Correct / Incorrect
    - Confidence
    - Inference time
    - Timestamp
    """


    def __init__(
        self,
        student_id="default_student"
    ):

        self.student_id = student_id

        self.attempts = []


    # =====================================================
    # Record Complete Attempt
    # Used by AssessmentService
    # =====================================================

    def record_attempt(
        self,
        attempt_data
    ):

        expected = attempt_data.get(
            "expected",
            "UNKNOWN"
        )

        predicted = attempt_data.get(
            "predicted",
            "UNKNOWN"
        )

        correct = attempt_data.get(
            "correct",
            False
        )

        confidence = attempt_data.get(
            "confidence",
            0
        )


        motion_metrics = attempt_data.get(
            "motion_metrics",
            {}
        )


        # Convert confidence to percentage

        if confidence <= 1:

            confidence = confidence * 100



        attempt = {


            "student_id":
                self.student_id,


            "expected_alphabet":
                str(expected).upper(),


            "predicted_alphabet":
                str(predicted).upper(),


            "correct":
                bool(correct),


            "confidence":
                round(
                    confidence,
                    2
                ),


            "inference_time_ms":
                round(
                    motion_metrics.get(
                        "average_latency",
                        0
                    ),
                    2
                ),


            "motion_metrics":
                motion_metrics,


            "timestamp":
                datetime.now().isoformat()

        }


        self.attempts.append(
            attempt
        )


        return attempt



    # =====================================================
    # Legacy Add Attempt
    # =====================================================

    def add_attempt(
        self,
        expected,
        predicted,
        correct,
        confidence,
        inference_time
    ):


        if confidence <= 1:

            confidence *= 100



        attempt = {


            "student_id":
                self.student_id,


            "expected_alphabet":
                str(expected).upper(),


            "predicted_alphabet":
                str(predicted).upper(),


            "correct":
                bool(correct),


            "confidence":
                round(
                    confidence,
                    2
                ),


            "inference_time_ms":
                round(
                    inference_time,
                    2
                ),


            "timestamp":
                datetime.now().isoformat()

        }


        self.attempts.append(
            attempt
        )


        return attempt



    # =====================================================
    # Get Complete History
    # =====================================================

    def get_history(self):

        return self.attempts



    # =====================================================
    # Total Attempts
    # =====================================================

    def count(self):

        return len(
            self.attempts
        )



    # =====================================================
    # Correct Attempts
    # =====================================================

    def correct_count(self):

        return sum(

            1

            for attempt in self.attempts

            if attempt["correct"]

        )



    # =====================================================
    # Incorrect Attempts
    # =====================================================

    def incorrect_count(self):

        return sum(

            1

            for attempt in self.attempts

            if not attempt["correct"]

        )



    # =====================================================
    # Accuracy
    # =====================================================

    def accuracy(self):


        if not self.attempts:

            return 0



        return round(

            (
                self.correct_count()

                /

                len(self.attempts)

            )

            * 100,

            2

        )



    # =====================================================
    # Alphabet Specific History
    # =====================================================

    def get_alphabet_history(
        self,
        alphabet
    ):

        alphabet = str(
            alphabet
        ).upper()


        return [

            attempt

            for attempt in self.attempts

            if attempt[
                "expected_alphabet"
            ] == alphabet

        ]



    # =====================================================
    # Clear Attempts
    # =====================================================

    def clear(self):

        self.attempts.clear()