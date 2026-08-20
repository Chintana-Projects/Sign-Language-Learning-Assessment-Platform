from .rule_base import GestureRule


class RuleY(GestureRule):
    """
    ASL Alphabet Y

    Expected:
    - Thumb extended
    - Pinky extended
    - Index folded
    - Middle folded
    - Ring folded
    """

    def __init__(self):
        super().__init__("Y")

    def evaluate(self, landmarks, deviations, messages):

        if not landmarks or len(landmarks) != 21:
            deviations.append("Invalid hand landmarks.")
            messages.append("Show your complete hand.")
            return False

        # Folded fingers
        if landmarks[8][1] < landmarks[6][1]:
            deviations.append("Index finger should be folded.")

        if landmarks[12][1] < landmarks[10][1]:
            deviations.append("Middle finger should be folded.")

        if landmarks[16][1] < landmarks[14][1]:
            deviations.append("Ring finger should be folded.")

        # Pinky extended
        if landmarks[20][1] > landmarks[18][1]:
            deviations.append("Pinky finger should be extended.")

        # Thumb extended
        if abs(landmarks[4][0] - landmarks[3][0]) < 0.05:
            deviations.append("Thumb should be extended outward.")

        if deviations:
            messages.append(
                "Extend your thumb and pinky while folding the other fingers."
            )
            return False

        messages.append("Y gesture looks correct.")
        return True