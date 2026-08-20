from .rule_base import GestureRule


class RuleZ(GestureRule):
    """
    ASL Alphabet Z

    Expected:
    - Index finger extended
    - Other fingers folded

    Note:
    Dynamic movement (drawing 'Z' in air)
    cannot be verified using a single frame.
    """

    def __init__(self):
        super().__init__("Z")

    def evaluate(self, landmarks, deviations, messages):

        if not landmarks or len(landmarks) != 21:
            deviations.append("Invalid hand landmarks.")
            messages.append("Show your complete hand.")
            return False

        # Index extended
        if landmarks[8][1] > landmarks[6][1]:
            deviations.append("Index finger should be extended.")

        # Remaining folded
        if landmarks[12][1] < landmarks[10][1]:
            deviations.append("Middle finger should be folded.")

        if landmarks[16][1] < landmarks[14][1]:
            deviations.append("Ring finger should be folded.")

        if landmarks[20][1] < landmarks[18][1]:
            deviations.append("Pinky finger should be folded.")

        if deviations:
            messages.append(
                "Extend only your index finger before drawing the letter Z."
            )
            return False

        messages.append(
            "Hand shape for Z is correct. Draw the Z motion to complete the sign."
        )

        return True