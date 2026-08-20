class SequenceGenerator:
    """
    Converts buffered landmark frames
    into sequences suitable for future
    LSTM / GRU / Transformer models.

    Input:
        List of frames

        Example:
        [
            [63 features],
            [63 features],
            ...
        ]

    Output:
        Sequence batch

        Example:
        [
            [
                [63 features],
                [63 features],
                ...
            ]
        ]
    """


    def __init__(self, sequence_length=30):

        self.sequence_length = sequence_length


    # --------------------------------------------------
    # Generate sequence
    # --------------------------------------------------

    def generate(self, frames):

        if len(frames) < self.sequence_length:

            raise ValueError(
                f"Need {self.sequence_length} frames, "
                f"received {len(frames)}"
            )


        # Take latest N frames

        sequence = frames[
            -self.sequence_length:
        ]


        return sequence


    # --------------------------------------------------
    # Generate model batch
    # --------------------------------------------------

    def generate_batch(self, frames):

        sequence = self.generate(frames)


        # Add batch dimension

        return [
            sequence
        ]