from .rule_base import GestureRule


class RuleA(GestureRule):

    """
    ASL Alphabet A Rule

    Expected:
    - Four fingers folded
    - Thumb outside fist
    """


    def __init__(self):

        super().__init__("A")



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



        folded_count = 0



        for finger, folded in fingers.items():


            if folded:

                folded_count += 1


            else:

                deviations.append(

                    f"{finger} finger should be folded."

                )



        # Better combined feedback

        if folded_count < 4:


            messages.append(

                "Close your fingers into a fist for A gesture."

            )



        # Thumb check

        thumb_tip = landmarks[4]

        index_base = landmarks[5]



        if thumb_tip[1] > index_base[1]:


            deviations.append(

                "Thumb position incorrect."

            )


            messages.append(

                "Place your thumb outside the folded fingers."

            )



        if not deviations:


            messages.append(

                "A gesture finger position looks correct."

            )


            return True



        return False