from .rule_base import GestureRule


class RuleQ(GestureRule):
    """
    ASL Alphabet Q

    Expected:
    - Index extended downward
    - Thumb extended
    - Other fingers folded
    """

    def __init__(self):
        super().__init__("Q")

    def evaluate(self, landmarks, deviations, messages):

        if not landmarks or len(landmarks) != 21:
            deviations.append("Invalid hand landmarks.")
            messages.append("Show your complete hand.")
            return False

        if landmarks[8][1] > landmarks[6][1]:
            deviations.append("Index finger should be extended.")

        if landmarks[12][1] < landmarks[10][1]:
            deviations.append("Middle finger should be folded.")

        if landmarks[16][1] < landmarks[14][1]:
            deviations.append("Ring finger should be folded.")

        if landmarks[20][1] < landmarks[18][1]:
            deviations.append("Pinky finger should be folded.")

        if deviations:
            messages.append("Extend your index finger and fold the remaining fingers.")
            return False

        messages.append("Q gesture looks correct.")
        return True