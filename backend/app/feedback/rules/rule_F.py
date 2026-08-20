from .rule_base import GestureRule
import math


class RuleF(GestureRule):
    """
    ASL Alphabet F Gesture Rule

    Expected:
    - Thumb and index finger touching
    - Middle finger extended
    - Ring finger extended
    - Pinky finger extended
    """

    def __init__(self):
        super().__init__("F")

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
        # Thumb touching Index
        # -----------------------------------------

        thumb_tip = landmarks[4]
        index_tip = landmarks[8]

        gap = math.dist(
            (thumb_tip[0], thumb_tip[1]),
            (index_tip[0], index_tip[1])
        )

        if gap > 0.05:

            deviations.append(
                "Thumb and index finger should touch."
            )

            messages.append(
                "Touch your thumb and index finger together."
            )

        # -----------------------------------------
        # Other fingers extended
        # -----------------------------------------

        fingers = {

            "Middle":
                landmarks[12][1] < landmarks[10][1],

            "Ring":
                landmarks[16][1] < landmarks[14][1],

            "Pinky":
                landmarks[20][1] < landmarks[18][1]

        }

        for finger, extended in fingers.items():

            if not extended:

                deviations.append(
                    f"{finger} finger should be extended."
                )

                messages.append(
                    f"Straighten your {finger.lower()} finger."
                )

        # -----------------------------------------
        # Success
        # -----------------------------------------

        if not deviations:

            messages.append(
                "F gesture finger position looks correct."
            )

            return True

        return False