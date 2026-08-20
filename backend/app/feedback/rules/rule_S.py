from .rule_base import GestureRule


class RuleS(GestureRule):
    """
    ASL Alphabet S

    Expected:
    - All fingers folded
    - Thumb wrapped over fingers
    """

    def __init__(self):
        super().__init__("S")

    def evaluate(self, landmarks, deviations, messages):

        if not landmarks or len(landmarks) != 21:
            deviations.append("Invalid hand landmarks.")
            messages.append("Show your complete hand.")
            return False

        fingers_folded = [
            landmarks[8][1] > landmarks[6][1],
            landmarks[12][1] > landmarks[10][1],
            landmarks[16][1] > landmarks[14][1],
            landmarks[20][1] > landmarks[18][1]
        ]

        if not all(fingers_folded):
            deviations.append("All fingers should be folded.")

        thumb_tip = landmarks[4]
        index_mcp = landmarks[5]

        if thumb_tip[1] < index_mcp[1]:
            deviations.append("Thumb should wrap over the fingers.")

        if deviations:
            messages.append("Close your hand into a fist and wrap the thumb over the fingers.")
            return False

        messages.append("S gesture looks correct.")
        return True