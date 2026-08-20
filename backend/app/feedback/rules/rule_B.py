from .rule_base import GestureRule


class RuleB(GestureRule):
    """
    ASL Alphabet B Gesture Rule

    Expected:
    - Index finger extended
    - Middle finger extended
    - Ring finger extended
    - Pinky finger extended
    - Fingers close together
    - Thumb folded across palm
    """

    def __init__(self):

        super().__init__("B")



    # =====================================================
    # Evaluate B Gesture
    # =====================================================

    def evaluate(
            self,
            landmarks,
            deviations,
            messages
    ):


        # -----------------------------------------
        # Validate landmarks
        # -----------------------------------------

        if not landmarks or len(landmarks) != 21:

            deviations.append(
                "Invalid hand landmarks."
            )

            messages.append(
                "Show your complete hand."
            )

            return False



        # -----------------------------------------
        # Check finger extension
        # -----------------------------------------

        fingers = {


            "Index":

                landmarks[8][1] < landmarks[6][1],



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
        # Check fingers are together
        # -----------------------------------------

        index_tip = landmarks[8]

        middle_tip = landmarks[12]


        finger_gap = abs(

            index_tip[0]

            -

            middle_tip[0]

        )



        if finger_gap > 0.10:


            deviations.append(

                "Fingers are separated."

            )


            messages.append(

                "Keep your fingers straight and together."

            )



        # -----------------------------------------
        # Check thumb position
        # -----------------------------------------

        thumb_tip = landmarks[4]

        thumb_ip = landmarks[3]



        # Thumb should cross palm

        if thumb_tip[0] > thumb_ip[0]:


            deviations.append(

                "Thumb position incorrect."

            )


            messages.append(

                "Place your thumb across your palm."

            )



        # -----------------------------------------
        # Return result
        # -----------------------------------------

        # No success messages here.
        # FeedbackEngine handles success.

        return len(deviations) == 0