from .rule_base import GestureRule


class RuleN(GestureRule):
    """
    ASL Alphabet N

    Expected:
    - All fingers folded
    - Thumb tucked under first two fingers
    """

    def __init__(self):
        super().__init__("N")

    def evaluate(self, landmarks, deviations, messages):

        if not landmarks or len(landmarks) != 21:
            deviations.append("Invalid hand landmarks.")
            messages.append("Show your complete hand.")
            return False

        folded = [
            landmarks[8][1] > landmarks[6][1],
            landmarks[12][1] > landmarks[10][1],
            landmarks[16][1] > landmarks[14][1],
            landmarks[20][1] > landmarks[18][1]
        ]

        if not all(folded):
            deviations.append("All fingers should be folded.")

        thumb = landmarks[4][1]

        if thumb < landmarks[8][1]:
            deviations.append("Thumb should rest beneath the first two fingers.")

        if deviations:
            messages.append("Fold your fingers and tuck the thumb under the index and middle fingers.")
            return False

        messages.append("N gesture looks correct.")
        return True