from collections import deque
import numpy as np



class TemporalBuffer:
    """
    SignSync Temporal Buffer

    Purpose:
    --------
    Stores continuous landmark frames from webcam.

    Used for future temporal models:
    - LSTM
    - GRU
    - Transformer
    - TCN


    Features:
    --------
    ✔ Stores latest N frames
    ✔ Removes oldest frame automatically
    ✔ Provides complete gesture sequence
    ✔ Converts sequence to ML-ready array
    """



    def __init__(self, max_frames: int = 30):

        self.max_frames = max_frames

        self.buffer = deque(
            maxlen=max_frames
        )





    # =================================================
    # Add Landmark Frame
    # =================================================

    def add_frame(self, landmarks):
        """
        Add one frame.

        Expected:

        [
            [x,y,z],
            [x,y,z],
            ...
            21 points
        ]

        OR

        [
            63 features
        ]
        """


        if landmarks is None:

            return False



        try:

            array = np.array(
                landmarks,
                dtype=float
            )


        except Exception:

            return False




        # Accept 21x3 landmarks

        if array.shape == (21,3):

            self.buffer.append(
                landmarks
            )

            return True




        # Accept flattened 63 features

        if array.shape == (63,):

            self.buffer.append(
                landmarks
            )

            return True




        return False







    # =================================================
    # Get Complete Sequence
    # =================================================

    def get_sequence(self):
        """
        Returns:

        [
            frame1,
            frame2,
            ...
            frame30
        ]
        """

        return list(
            self.buffer
        )







    # =================================================
    # Get ML Ready Sequence
    # =================================================

    def get_sequence_array(self):

        """
        Returns numpy array.

        Example:

        (30,21,3)

        for temporal models.
        """


        if not self.buffer:

            return np.array([])



        return np.array(

            self.buffer,

            dtype=float

        )







    # =================================================
    # Latest Frame
    # =================================================

    def get_latest_frame(self):

        if not self.buffer:

            return None


        return self.buffer[-1]








    # =================================================
    # Buffer Size
    # =================================================

    def size(self):

        return len(
            self.buffer
        )






    # =================================================
    # Full Check
    # =================================================

    def is_full(self):

        return (

            len(self.buffer)

            ==

            self.max_frames

        )







    # =================================================
    # Empty Check
    # =================================================

    def is_empty(self):

        return len(
            self.buffer
        ) == 0







    # =================================================
    # Clear
    # =================================================

    def clear(self):

        self.buffer.clear()







    # =================================================
    # Python length support
    # =================================================

    def __len__(self):

        return len(
            self.buffer
        )








# =================================================
# Test
# =================================================

if __name__ == "__main__":


    buffer = TemporalBuffer(
        max_frames=5
    )


    for i in range(7):

        fake_landmark = [

            [i,i,i]

            for _ in range(21)

        ]


        buffer.add_frame(
            fake_landmark
        )



    print(
        "Buffer size:",
        buffer.size()
    )


    print(
        "Sequence shape:",
        buffer.get_sequence_array().shape
    )


    print(
        "Latest frame:",
        buffer.get_latest_frame()
    )