from .rule_base import GestureRule


class RuleD(GestureRule):
    """
    ASL Alphabet D Gesture Rule

    Expected:
    - Index finger extended
    - Middle finger folded
    - Ring finger folded
    - Pinky finger folded
    - Thumb touching the folded fingers
    """

    def __init__(self):
        super().__init__("D")

    def evaluate(
            self,
            landmarks,
            deviations,
            messages
    ):

        if not landmarks or len(landmarks) != 21:

            deviations.append(
                "Invalid hand landmarks."
            )

            messages.append(
                "Show your complete hand."
            )

            return False

        # -----------------------------------------
        # Finger states
        # -----------------------------------------

        index_extended = landmarks[8][1] < landmarks[6][1]

        middle_folded = landmarks[12][1] > landmarks[10][1]

        ring_folded = landmarks[16][1] > landmarks[14][1]

        pinky_folded = landmarks[20][1] > landmarks[18][1]

        if not index_extended:

            deviations.append(
                "Index finger should be extended."
            )

            messages.append(
                "Straighten your index finger."
            )

        if not middle_folded:

            deviations.append(
                "Middle finger should be folded."
            )

            messages.append(
                "Fold your middle finger."
            )

        if not ring_folded:

            deviations.append(
                "Ring finger should be folded."
            )

            messages.append(
                "Fold your ring finger."
            )

        if not pinky_folded:

            deviations.append(
                "Pinky finger should be folded."
            )

            messages.append(
                "Fold your pinky finger."
            )

        # -----------------------------------------
        # Thumb position
        # -----------------------------------------

        thumb_tip = landmarks[4]
        middle_mcp = landmarks[9]

        if abs(thumb_tip[0] - middle_mcp[0]) > 0.12:

            deviations.append(
                "Thumb position incorrect."
            )

            messages.append(
                "Keep your thumb touching the folded fingers."
            )

        # -----------------------------------------
        # Success
        # -----------------------------------------

        if not deviations:

            messages.append(
                "D gesture finger position looks correct."
            )

            return True

        return False