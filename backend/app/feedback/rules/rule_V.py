from .rule_base import GestureRule


class RuleV(GestureRule):
    """
    ASL Alphabet V

    Expected:
    - Index extended
    - Middle extended
    - Fingers separated
    - Ring folded
    - Pinky folded
    """

    def __init__(self):
        super().__init__("V")

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

        gap = abs(landmarks[8][0] - landmarks[12][0])

        if gap < 0.05:
            deviations.append("Separate your index and middle fingers.")

        if deviations:
            messages.append("Make a V shape using your index and middle fingers.")
            return False

        messages.append("V gesture looks correct.")
        return True