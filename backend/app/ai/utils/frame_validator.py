class FrameValidator:
    """
    SignSync Frame Validator

    Validates incoming webcam frames
    before ML inference.
    """

    def __init__(
        self,
        max_hands=1
    ):

        self.max_hands = max_hands



    def validate(
        self,
        detection_result
    ):

        """
        Input:

        {
            hand_count,
            person_count,
            body_visible,
            landmarks
        }


        Output:

        {
            valid: True/False,
            reason: message
        }

        """



        # -----------------------------
        # No person
        # -----------------------------

        if detection_result["person_count"] == 0:

            return {

                "valid": False,

                "reason":
                "No person detected"

            }



        # -----------------------------
        # Body visibility
        # -----------------------------

        if not detection_result["body_visible"]:

            return {

                "valid": False,

                "reason":
                "Body not visible"

            }



        # -----------------------------
        # No hand
        # -----------------------------

        if detection_result["hand_count"] == 0:

            return {

                "valid": False,

                "reason":
                "No hand detected"

            }



        # -----------------------------
        # Multiple hands
        # -----------------------------

        if detection_result["hand_count"] > self.max_hands:

            return {

                "valid": False,

                "reason":
                "Multiple hands detected"

            }



        # -----------------------------
        # Landmark validation
        # -----------------------------

        landmarks = detection_result["landmarks"]


        if not landmarks:

            return {

                "valid": False,

                "reason":
                "Empty landmarks"

            }



        if len(landmarks[0]) != 21:

            return {

                "valid": False,

                "reason":
                "Incomplete hand landmarks"

            }



        return {

            "valid": True,

            "reason":
            "Frame valid"

        }