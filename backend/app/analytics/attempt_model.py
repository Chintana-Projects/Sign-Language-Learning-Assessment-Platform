from datetime import datetime


class AttemptModel:
    """
    Represents one student practice attempt.

    Stores:
    - Student ID
    - Expected alphabet
    - Predicted alphabet
    - Correctness
    - Confidence
    - Inference time
    - Timestamp
    """


    def __init__(
            self,
            student_id,
            expected,
            predicted,
            correct,
            confidence,
            inference_time
    ):

        self.student_id = student_id

        self.expected = expected

        self.predicted = predicted

        self.correct = correct

        self.confidence = confidence

        self.inference_time = inference_time

        self.timestamp = (
            datetime.now()
            .isoformat()
        )



    # -----------------------------------------
    # Convert to dictionary
    # -----------------------------------------

    def to_dict(self):

        return {

            "student":
                self.student_id,

            "expected":
                self.expected,

            "predicted":
                self.predicted,

            "correct":
                self.correct,

            "confidence":
                self.confidence,

            "inference_time":
                self.inference_time,

            "timestamp":
                self.timestamp

        }