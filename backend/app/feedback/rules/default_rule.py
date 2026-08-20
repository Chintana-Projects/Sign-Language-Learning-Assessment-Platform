from .rule_base import GestureRule


class DefaultRule(GestureRule):

    """
    Fallback rule for gestures
    without specific implementation.
    """


    def __init__(self, gesture):

        super().__init__(gesture)



    def evaluate(
            self,
            landmarks,
            deviations,
            messages
    ):


        if not landmarks or len(landmarks) != 21:


            deviations.append(
                "Invalid landmark data."
            )


            messages.append(
                "Keep your complete hand visible."
            )


            return False



        messages.append(

            f"{self.gesture} gesture analysis completed."

        )


        return True