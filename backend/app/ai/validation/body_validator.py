class BodyValidator:
    """
    SignSync Body Validator

    Checks human body visibility before gesture recognition.

    Validations:
    - NO_PERSON
    - PARTIAL_BODY
    - VALID_BODY

    Future:
    - MULTIPLE_PEOPLE
    """

    def __init__(self):

        # Minimum pose landmark visibility
        self.minimum_visibility = 0.5


    # ==================================================
    # Validate Body
    # ==================================================

    def validate(
            self,
            pose_landmarks,
            person_count=1
    ):


        # ------------------------------------------
        # No person detected
        # ------------------------------------------

        if pose_landmarks is None:

            return {

                "valid": False,

                "reason": "NO_PERSON",

                "message":
                    "No person detected."

            }



        # ------------------------------------------
        # Multiple People
        # ------------------------------------------

        if person_count > 1:

            return {

                "valid": False,

                "reason": "MULTIPLE_PEOPLE",

                "message":
                    "Only one person should be visible."

            }



        # ------------------------------------------
        # Required Upper Body Points
        # ------------------------------------------

        required_landmarks = [

            11,   # Left shoulder

            12,   # Right shoulder

            13,   # Left elbow

            14,   # Right elbow

            15,   # Left wrist

            16    # Right wrist

        ]



        missing_points = []



        for index in required_landmarks:


            try:

                visibility = (
                    pose_landmarks[index]
                    .visibility
                )


                if visibility < self.minimum_visibility:

                    missing_points.append(index)



            except Exception:


                missing_points.append(index)




        # ------------------------------------------
        # Partial Body
        # ------------------------------------------

        if len(missing_points) > 0:


            return {


                "valid": False,


                "reason":
                    "PARTIAL_BODY",


                "missing_landmarks":
                    missing_points,


                "message":
                    "Please keep your upper body visible."

            }



        # ------------------------------------------
        # Valid Body
        # ------------------------------------------

        return {


            "valid": True,


            "reason":
                "VALID_BODY",


            "message":
                "Body visibility acceptable."

        }