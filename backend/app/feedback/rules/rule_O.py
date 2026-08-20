from .rule_base import GestureRule
import math


class RuleO(GestureRule):
    """
    ASL Alphabet O

    Expected:
    - Thumb touching index finger
    - Fingers curved forming O
    """

    def __init__(self):
        super().__init__("O")

    def evaluate(self, landmarks, deviations, messages):

        if not landmarks or len(landmarks) != 21:
            deviations.append("Invalid hand landmarks.")
            messages.append("Show your complete hand.")
            return False

        thumb_tip = landmarks[4]
        index_tip = landmarks[8]

        gap = math.dist(
            (thumb_tip[0], thumb_tip[1]),
            (index_tip[0], index_tip[1])
        )

        if gap > 0.05:
            deviations.append("Thumb and index finger should touch.")

        extended = [
            landmarks[12][1] < landmarks[10][1],
            landmarks[16][1] < landmarks[14][1],
            landmarks[20][1] < landmarks[18][1]
        ]

        if not all(extended):
            deviations.append("Curve the remaining fingers to complete the O shape.")

        if deviations:
            messages.append("Touch your thumb and index finger to form an O.")
            return False

        messages.append("O gesture looks correct.")
        return True