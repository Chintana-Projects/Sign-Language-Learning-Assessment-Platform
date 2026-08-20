class LandmarkConverter:

    @staticmethod
    def to_model_format(hand_landmarks):

        if not hand_landmarks:
            raise ValueError(
                "No hand landmarks provided."
            )


        # Already in [x,y,z] format
        if (
            isinstance(hand_landmarks, list)
            and len(hand_landmarks)==21
            and isinstance(hand_landmarks[0], list)
        ):

            if len(hand_landmarks[0]) == 3:

                return [
                    [
                        float(point[0]),
                        float(point[1]),
                        float(point[2])
                    ]

                    for point in hand_landmarks
                ]



        # Dictionary format

        if len(hand_landmarks) != 21:

            raise ValueError(
                f"Expected 21 landmarks, received {len(hand_landmarks)}"
            )


        landmarks=[]


        for landmark in hand_landmarks:

            landmarks.append(
                [
                    float(landmark["x"]),
                    float(landmark["y"]),
                    float(landmark["z"])
                ]
            )


        return landmarks