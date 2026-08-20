from .rule_base import GestureRule


class RuleH(GestureRule):
    """
    ASL Alphabet H

    Expected:
    - Index extended
    - Middle extended
    - Ring folded
    - Pinky folded
    """

    def __init__(self):
        super().__init__("H")

    def evaluate(self, landmarks, deviations, messages):

        if not landmarks or len(landmarks) != 21:
            deviations.append("Invalid hand landmarks.")
            messages.append("Show your complete hand.")
            return False

        if landmarks[8][1] > landmarks[6][1]:
            deviations.append("Index finger should be extended.")
            messages.append("Straighten your index finger.")

        if landmarks[12][1] > landmarks[10][1]:
            deviations.append("Middle finger should be extended.")
            messages.append("Straighten your middle finger.")

        if landmarks[16][1] < landmarks[14][1]:
            deviations.append("Ring finger should be folded.")
            messages.append("Fold your ring finger.")

        if landmarks[20][1] < landmarks[18][1]:
            deviations.append("Pinky finger should be folded.")
            messages.append("Fold your pinky finger.")

        if not deviations:
            messages.append("H gesture finger position looks correct.")
            return True

        return False