class SentenceBuilder:
    """
    Builds words and sentences from
    sequential gesture predictions.

    Current:
        A
        B
        C

    Future:
        HELLO
        HOW ARE YOU
    """

    def __init__(self):

        self.tokens = []

    # ----------------------------------------
    # Add predicted gesture
    # ----------------------------------------

    def add_prediction(self, gesture):

        self.tokens.append(gesture)

    # ----------------------------------------
    # Return sentence
    # ----------------------------------------

    def get_sentence(self):

        return " ".join(self.tokens)

    # ----------------------------------------
    # Clear sentence
    # ----------------------------------------

    def clear(self):

        self.tokens.clear()

    # ----------------------------------------
    # Number of stored predictions
    # ----------------------------------------

    def size(self):

        return len(self.tokens)