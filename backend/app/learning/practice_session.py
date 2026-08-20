import time
from datetime import datetime


class PracticeSession:
    """
    Manages a single alphabet practice session.

    Responsibilities:
    - Store expected alphabet
    - Compare prediction
    - Track attempts
    - Calculate accuracy
    - Track gesture completion time
    - Track confidence metrics
    - Track invalid frames
    - Move to next question
    """


    def __init__(self, alphabet):

        self.expected_letter = alphabet.upper()


        # -------------------------------
        # Attempt Tracking
        # -------------------------------

        self.attempts = 0

        self.correct_attempts = 0

        self.history = []



        # -------------------------------
        # Motion Metrics
        # -------------------------------

        self.gesture_start_time = time.time()

        self.gesture_end_time = None

        self.time_taken = 0



        # Confidence Tracking

        self.confidence_history = []

        self.total_confidence = 0



        # Invalid Frames

        self.invalid_frames = 0




    # -----------------------------------------
    # Invalid frame tracking
    # -----------------------------------------

    def add_invalid_frame(self):

        """
        Called when webcam frame has:
        - no hand
        - multiple hands
        - failed prediction
        """

        self.invalid_frames += 1





    # -----------------------------------------
    # Check prediction
    # -----------------------------------------

    def evaluate_prediction(
            self,
            predicted_letter,
            confidence
    ):


        self.attempts += 1


        predicted_letter = predicted_letter.upper()



        is_correct = (

            predicted_letter ==
            self.expected_letter

        )



        if is_correct:

            self.correct_attempts += 1




        # -------------------------------
        # Gesture Completion Time
        # -------------------------------

        self.gesture_end_time = time.time()



        self.time_taken = round(

            self.gesture_end_time -
            self.gesture_start_time,

            2

        )





        # -------------------------------
        # Confidence Metrics
        # -------------------------------

        self.confidence_history.append(
            confidence
        )


        self.total_confidence += confidence



        average_confidence = round(

            self.total_confidence /
            len(self.confidence_history),

            2

        )





        result = {


            "expected":
                self.expected_letter,


            "predicted":
                predicted_letter,


            "correct":
                is_correct,



            "confidence":
                confidence,



            "average_confidence":
                average_confidence,



            "time_taken":
                self.time_taken,



            "invalid_frames":
                self.invalid_frames,



            "attempt_number":
                self.attempts,



            "timestamp":
                datetime.now().isoformat()

        }




        self.history.append(result)




        # Reset values for next gesture

        self.gesture_start_time = time.time()


        self.invalid_frames = 0



        return result





    # -----------------------------------------
    # Current accuracy
    # -----------------------------------------

    def get_accuracy(self):


        if self.attempts == 0:

            return 0.0



        return round(

            (

                self.correct_attempts /
                self.attempts

            ) * 100,

            2

        )






    # -----------------------------------------
    # Average Confidence
    # -----------------------------------------

    def get_average_confidence(self):


        if not self.confidence_history:

            return 0



        return round(

            sum(self.confidence_history)
            /
            len(self.confidence_history),

            2

        )







    # -----------------------------------------
    # Change question
    # -----------------------------------------

    def change_letter(
            self,
            new_letter
    ):


        self.expected_letter = (

            new_letter.upper()

        )



        # Restart gesture timer

        self.gesture_start_time = time.time()


        self.invalid_frames = 0





    # -----------------------------------------
    # Session summary
    # -----------------------------------------

    def summary(self):


        return {


            "current_letter":
                self.expected_letter,



            "total_attempts":
                self.attempts,



            "correct":
                self.correct_attempts,



            "incorrect":
                self.attempts -
                self.correct_attempts,



            "accuracy":
                self.get_accuracy(),



            "average_confidence":
                self.get_average_confidence(),



            "history":
                self.history



        }