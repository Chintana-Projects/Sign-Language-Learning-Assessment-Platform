from .rule_base import GestureRule


class RuleM(GestureRule):
    """
    ASL Alphabet M

    Expected:
    - All fingers folded
    - Thumb tucked under three fingers
    """

    def __init__(self):
        super().__init__("M")

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

        if thumb < landmarks[10][1]:
            deviations.append("Thumb should be tucked under the fingers.")

        if deviations:
            messages.append("Fold all fingers and tuck your thumb under them.")
            return False

        messages.append("M gesture looks correct.")
        return True