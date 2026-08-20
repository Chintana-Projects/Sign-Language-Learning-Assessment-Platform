from .rule_base import GestureRule


class RuleL(GestureRule):
    """
    ASL Alphabet L

    Expected:
    - Index extended
    - Thumb extended
    - Middle folded
    - Ring folded
    - Pinky folded
    """

    def __init__(self):
        super().__init__("L")

    def evaluate(self, landmarks, deviations, messages):

        if not landmarks or len(landmarks) != 21:
            deviations.append("Invalid hand landmarks.")
            messages.append("Show your complete hand.")
            return False

        if landmarks[8][1] > landmarks[6][1]:
            deviations.append("Index finger should be extended.")
            messages.append("Straighten your index finger.")

        if abs(landmarks[4][0] - landmarks[2][0]) < 0.08:
            deviations.append("Thumb should be extended.")
            messages.append("Extend your thumb outward.")

        if landmarks[12][1] < landmarks[10][1]:
            deviations.append("Middle finger should be folded.")
            messages.append("Fold your middle finger.")

        if landmarks[16][1] < landmarks[14][1]:
            deviations.append("Ring finger should be folded.")
            messages.append("Fold your ring finger.")

        if landmarks[20][1] < landmarks[18][1]:
            deviations.append("Pinky finger should be folded.")
            messages.append("Fold your pinky finger.")

        if not deviations:
            messages.append("L gesture finger position looks correct.")
            return True

        return False