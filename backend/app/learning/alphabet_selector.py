class AlphabetSelector:
    """
    Handles alphabet selection for practice sessions.

    Supports:
    A-Z alphabet gestures.
    """

    def __init__(self):

        self.alphabets = [
            chr(i) for i in range(ord('A'), ord('Z') + 1)
        ]

    # -----------------------------------------
    # Get all available letters
    # -----------------------------------------

    def get_all_letters(self):

        return self.alphabets


    # -----------------------------------------
    # Validate selected letter
    # -----------------------------------------

    def is_valid_letter(self, letter):

        return letter.upper() in self.alphabets


    # -----------------------------------------
    # Select practice letter
    # -----------------------------------------

    def select_letter(self, letter):

        letter = letter.upper()

        if not self.is_valid_letter(letter):

            raise ValueError(
                f"Invalid alphabet: {letter}"
            )

        return letter