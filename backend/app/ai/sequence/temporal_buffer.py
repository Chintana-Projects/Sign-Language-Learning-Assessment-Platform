from collections import deque


class TemporalBuffer:
    """
    Sequence Temporal Buffer.

    Used for storing feature vectors
    before passing data into temporal
    deep learning models.

    Models:
    - LSTM
    - GRU
    - Transformer
    """



    def __init__(self, max_frames=30):

        self.max_frames = max_frames

        self.buffer = deque(
            maxlen=max_frames
        )



    # -----------------------------------------
    # Add Frame
    # -----------------------------------------

    def add_frame(self, feature_vector):

        """
        Adds one 63-dimensional
        landmark feature vector.
        """


        if feature_vector is None:

            return False


        self.buffer.append(
            feature_vector
        )


        return True



    # -----------------------------------------
    # Get Sequence
    # -----------------------------------------

    def get_sequence(self):

        """
        Returns complete sequence
        for temporal models.
        """

        return list(
            self.buffer
        )



    # -----------------------------------------
    # Latest Frame
    # -----------------------------------------

    def get_latest_frame(self):

        if not self.buffer:

            return None


        return self.buffer[-1]



    # -----------------------------------------
    # Ready For Prediction
    # -----------------------------------------

    def is_ready(self):

        """
        Returns True when enough frames
        are collected for temporal inference.
        """

        return len(
            self.buffer
        ) >= self.max_frames



    # -----------------------------------------
    # Size
    # -----------------------------------------

    def size(self):

        return len(
            self.buffer
        )



    # -----------------------------------------
    # Clear
    # -----------------------------------------

    def clear(self):

        self.buffer.clear()



    # -----------------------------------------
    # Empty
    # -----------------------------------------

    def is_empty(self):

        return len(
            self.buffer
        ) == 0