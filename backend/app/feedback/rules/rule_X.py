from .rule_base import GestureRule


class RuleX(GestureRule):
    """
    ASL Alphabet X

    Expected:
    - Index bent like a hook
    - Other fingers folded
    """

    def __init__(self):
        super().__init__("X")

    def evaluate(self, landmarks, deviations, messages):

        if not landmarks or len(landmarks) != 21:
            deviations.append("Invalid hand landmarks.")
            messages.append("Show your complete hand.")
            return False

        index_bent = landmarks[8][1] < landmarks[6][1] and landmarks[7][1] > landmarks[6][1]

        if not index_bent:
            deviations.append("Index finger should be bent like a hook.")

        if landmarks[12][1] < landmarks[10][1]:
            deviations.append("Middle finger should be folded.")

        if landmarks[16][1] < landmarks[14][1]:
            deviations.append("Ring finger should be folded.")

        if landmarks[20][1] < landmarks[18][1]:
            deviations.append("Pinky finger should be folded.")

        if deviations:
            messages.append("Hook your index finger and fold the remaining fingers.")
            return False

        messages.append("X gesture looks correct.")
        return True