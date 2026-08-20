from .rule_base import GestureRule


class RuleR(GestureRule):
    """
    ASL Alphabet R

    Expected:
    - Index extended
    - Middle extended crossing index
    - Ring folded
    - Pinky folded
    """

    def __init__(self):
        super().__init__("R")

    def evaluate(self, landmarks, deviations, messages):

        if not landmarks or len(landmarks) != 21:
            deviations.append("Invalid hand landmarks.")
            messages.append("Show your complete hand.")
            return False

        if landmarks[8][1] > landmarks[6][1]:
            deviations.append("Index finger should be extended.")

        if landmarks[12][1] > landmarks[10][1]:
            deviations.append("Middle finger should be extended.")

        if landmarks[16][1] < landmarks[14][1]:
            deviations.append("Ring finger should be folded.")

        if landmarks[20][1] < landmarks[18][1]:
            deviations.append("Pinky finger should be folded.")

        if abs(landmarks[8][0] - landmarks[12][0]) > 0.05:
            deviations.append("Index and middle fingers should cross.")

        if deviations:
            messages.append("Cross your index and middle fingers while folding the others.")
            return False

        messages.append("R gesture looks correct.")
        return True