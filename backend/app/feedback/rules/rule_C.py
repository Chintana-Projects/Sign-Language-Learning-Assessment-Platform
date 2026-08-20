from .rule_base import GestureRule
import math


class RuleC(GestureRule):

    """
    ASL Alphabet C Gesture Rule

    Expected:
    - Fingers naturally curved
    - Thumb and index form open C shape
    - Moderate opening distance
    """


    def __init__(self):

        super().__init__("C")



    # =====================================================
    # Evaluate C Gesture
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
        # Thumb and index distance
        # -----------------------------------------

        thumb_tip = landmarks[4]

        index_tip = landmarks[8]



        gap = math.dist(

            (
                thumb_tip[0],
                thumb_tip[1]
            ),

            (
                index_tip[0],
                index_tip[1]
            )

        )



        # -----------------------------------------
        # Validate C opening
        # -----------------------------------------

        if gap < 0.05:


            deviations.append(

                "C shape is too closed."

            )


            messages.append(

                "Open your thumb and fingers slightly."

            )



        elif gap > 0.30:


            deviations.append(

                "C shape is too open."

            )


            messages.append(

                "Curve your fingers more to form C."

            )



        # -----------------------------------------
        # Check curved fingers
        # -----------------------------------------

        finger_angles = {


            "Index":

                self.calculate_angle(
                    landmarks[5],
                    landmarks[6],
                    landmarks[8]
                ),


            "Middle":

                self.calculate_angle(
                    landmarks[9],
                    landmarks[10],
                    landmarks[12]
                ),


            "Ring":

                self.calculate_angle(
                    landmarks[13],
                    landmarks[14],
                    landmarks[16]
                ),


            "Pinky":

                self.calculate_angle(
                    landmarks[17],
                    landmarks[18],
                    landmarks[20]
                )

        }



        for finger, angle in finger_angles.items():


            # Straight fingers usually have high angle.
            # C requires curved fingers.

            if angle > 170:


                deviations.append(

                    f"{finger} finger is too straight."

                )


                messages.append(

                    f"Curve your {finger.lower()} finger."

                )



        # -----------------------------------------
        # Return result
        # -----------------------------------------

        # No success message here.
        # FeedbackEngine handles success.

        return len(deviations) == 0



    # =====================================================
    # Helper Angle Function
    # =====================================================

    def calculate_angle(
            self,
            p1,
            p2,
            p3
    ):


        v1 = (

            p1[0] - p2[0],

            p1[1] - p2[1]

        )


        v2 = (

            p3[0] - p2[0],

            p3[1] - p2[1]

        )


        dot = (

            v1[0] * v2[0]

            +

            v1[1] * v2[1]

        )


        mag1 = math.sqrt(

            v1[0] ** 2 +

            v1[1] ** 2

        )


        mag2 = math.sqrt(

            v2[0] ** 2 +

            v2[1] ** 2

        )


        if mag1 == 0 or mag2 == 0:

            return 0



        cosine = dot / (mag1 * mag2)


        cosine = max(
            -1,
            min(
                1,
                cosine
            )
        )


        return math.degrees(
            math.acos(cosine)
        )