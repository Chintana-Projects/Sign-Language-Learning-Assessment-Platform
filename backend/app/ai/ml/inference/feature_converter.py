class FeatureConverter:
    """
    SignSync Feature Converter

    Converts MediaPipe hand landmarks:

    Input:
    [
        [x,y,z],
        ...
        21 landmarks
    ]

    Output:
    [
        x0,y0,z0,
        x1,y1,z1,
        ...
        x20,y20,z20
    ]

    Total features = 63
    """



    @staticmethod
    def to_feature_vector(
            landmarks
    ):


        # ---------------------------------
        # Validate input
        # ---------------------------------

        if landmarks is None:


            raise ValueError(

                "Landmarks cannot be None"

            )




        if len(landmarks) != 21:


            raise ValueError(

                f"Expected 21 landmarks, received {len(landmarks)}"

            )








        features = []






        # ---------------------------------
        # Flatten landmarks
        # ---------------------------------

        for index, point in enumerate(landmarks):


            if len(point) != 3:


                raise ValueError(

                    f"Landmark {index} must contain x,y,z"

                )



            x, y, z = point




            features.extend(

                [

                    float(x),

                    float(y),

                    float(z)

                ]

            )









        # ---------------------------------
        # Final safety check
        # ---------------------------------

        if len(features) != 63:


            raise ValueError(

                f"Feature vector must contain 63 values, got {len(features)}"

            )





        return features