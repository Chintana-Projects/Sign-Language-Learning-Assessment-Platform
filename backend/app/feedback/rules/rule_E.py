from .rule_base import GestureRule


class RuleE(GestureRule):
    """
    ASL Alphabet E Gesture Rule

    Expected:
    - All fingers folded
    - Fingertips close to the palm
    - Thumb folded across the fingers
    """

    def __init__(self):
        super().__init__("E")

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
        # All fingers folded
        # -----------------------------------------

        fingers = {

            "Index":
                landmarks[8][1] > landmarks[6][1],

            "Middle":
                landmarks[12][1] > landmarks[10][1],

            "Ring":
                landmarks[16][1] > landmarks[14][1],

            "Pinky":
                landmarks[20][1] > landmarks[18][1]

        }

        for finger, folded in fingers.items():

            if not folded:

                deviations.append(
                    f"{finger} finger should be folded."
                )

                messages.append(
                    f"Fold your {finger.lower()} finger."
                )

        # -----------------------------------------
        # Thumb folded
        # -----------------------------------------

        thumb_tip = landmarks[4]
        index_mcp = landmarks[5]

        if thumb_tip[0] < index_mcp[0]:

            deviations.append(
                "Thumb should be folded across the fingers."
            )

            messages.append(
                "Fold your thumb across the front of your fingers."
            )

        # -----------------------------------------
        # Success
        # -----------------------------------------

        if not deviations:

            messages.append(
                "E gesture finger position looks correct."
            )

            return True

        return False