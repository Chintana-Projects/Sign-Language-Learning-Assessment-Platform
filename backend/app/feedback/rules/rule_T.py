from .rule_base import GestureRule


class RuleT(GestureRule):
    """
    ASL Alphabet T

    Expected:
    - Fingers folded
    - Thumb between index and middle finger
    """

    def __init__(self):
        super().__init__("T")

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

        thumb_x = landmarks[4][0]
        index_x = landmarks[8][0]
        middle_x = landmarks[12][0]

        if not (min(index_x, middle_x) <= thumb_x <= max(index_x, middle_x)):
            deviations.append("Thumb should be between the index and middle finger.")

        if deviations:
            messages.append("Fold your fingers and place the thumb between the index and middle fingers.")
            return False

        messages.append("T gesture looks correct.")
        return True