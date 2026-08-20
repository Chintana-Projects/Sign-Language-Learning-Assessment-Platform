class FrameDetectionService:
    """
    SignSync Frame Detection Service

    Detects whether a webcam frame is usable before
    sending the landmarks to gesture recognition.

    IMPORTANT:
    The returned structure is compatible with
    AssessmentService.process_frame().
    """

    def __init__(self):

        self.edge_margin = 0.01

        self.minimum_hand_size = 0.03

        self.minimum_visible_landmarks = 15

    # ==================================================
    # DETECT
    # ==================================================

    def detect(
        self,
        landmarks,
        hand_count=1,
        person_count=1,
        body_visible=True
    ):
        """
        Analyze one webcam frame.

        Returns:

        {
            "valid": True/False,
            "reason": "...",
            "validation": {
                "valid": True/False,
                "reason": "..."
            }
        }
        """

        print("\n========== FRAME DETECTION ==========")

        print("Hand Count   :", hand_count)
        print("Person Count :", person_count)
        print("Body Visible :", body_visible)

        print(
            "Landmarks    :",
            len(landmarks)
            if landmarks is not None
            else 0
        )

        # --------------------------------------------------
        # NO PERSON
        # --------------------------------------------------

        if person_count == 0:

            return self._result(
                valid=False,
                reason="NO_PERSON_DETECTED",
                hand_count=hand_count,
                person_count=person_count,
                body_visible=body_visible
            )

        # --------------------------------------------------
        # MULTIPLE PEOPLE
        # --------------------------------------------------

        if person_count > 1:

            return self._result(
                valid=False,
                reason="MULTIPLE_PEOPLE",
                hand_count=hand_count,
                person_count=person_count,
                body_visible=body_visible
            )

        # --------------------------------------------------
        # PARTIAL BODY
        # --------------------------------------------------

        if not body_visible:

            return self._result(
                valid=False,
                reason="PARTIAL_BODY",
                hand_count=hand_count,
                person_count=person_count,
                body_visible=body_visible
            )

        # --------------------------------------------------
        # NO HAND
        # --------------------------------------------------

        if landmarks is None:

            return self._result(
                valid=False,
                reason="NO_HAND_DETECTED",
                hand_count=hand_count,
                person_count=person_count,
                body_visible=body_visible
            )

        if len(landmarks) == 0:

            return self._result(
                valid=False,
                reason="NO_HAND_DETECTED",
                hand_count=hand_count,
                person_count=person_count,
                body_visible=body_visible
            )

        # --------------------------------------------------
        # MULTIPLE HANDS
        # --------------------------------------------------

        if hand_count > 1:

            return self._result(
                valid=False,
                reason="MULTIPLE_HANDS",
                hand_count=hand_count,
                person_count=person_count,
                body_visible=body_visible
            )

        # --------------------------------------------------
        # LANDMARK COUNT
        # --------------------------------------------------

        if len(landmarks) != 21:

            return self._result(
                valid=False,
                reason="INVALID_LANDMARKS",
                hand_count=hand_count,
                person_count=person_count,
                body_visible=body_visible,
                landmark_count=len(landmarks)
            )

        # --------------------------------------------------
        # LANDMARK STRUCTURE
        # --------------------------------------------------

        for point in landmarks:

            if not isinstance(
                point,
                (list, tuple)
            ):

                return self._result(
                    valid=False,
                    reason="INVALID_LANDMARKS",
                    hand_count=hand_count,
                    person_count=person_count,
                    body_visible=body_visible
                )

            if len(point) < 2:

                return self._result(
                    valid=False,
                    reason="INVALID_LANDMARKS",
                    hand_count=hand_count,
                    person_count=person_count,
                    body_visible=body_visible
                )

        # --------------------------------------------------
        # COORDINATES
        # --------------------------------------------------

        try:

            xs = [
                float(point[0])
                for point in landmarks
            ]

            ys = [
                float(point[1])
                for point in landmarks
            ]

        except (
            TypeError,
            ValueError
        ):

            return self._result(
                valid=False,
                reason="INVALID_LANDMARKS",
                hand_count=hand_count,
                person_count=person_count,
                body_visible=body_visible
            )

        # --------------------------------------------------
        # VISIBLE LANDMARKS
        # --------------------------------------------------

        visible_landmarks = 0

        for x, y in zip(xs, ys):

            if (
                0 <= x <= 1
                and
                0 <= y <= 1
            ):

                visible_landmarks += 1

        if (
            visible_landmarks
            <
            self.minimum_visible_landmarks
        ):

            return self._result(
                valid=False,
                reason="PARTIAL_HAND",
                hand_count=hand_count,
                person_count=person_count,
                body_visible=body_visible,
                landmark_count=len(landmarks),
                visible_landmarks=visible_landmarks
            )

        # --------------------------------------------------
        # HAND SIZE
        # --------------------------------------------------

        width = max(xs) - min(xs)

        height = max(ys) - min(ys)

        # --------------------------------------------------
        # WARNINGS
        # --------------------------------------------------

        warnings = []

        if (
            min(xs) < self.edge_margin
            or
            max(xs) > (
                1 - self.edge_margin
            )
            or
            min(ys) < self.edge_margin
            or
            max(ys) > (
                1 - self.edge_margin
            )
        ):

            warnings.append(
                "HAND_OUTSIDE_FRAME"
            )

        if (
            width < self.minimum_hand_size
            or
            height < self.minimum_hand_size
        ):

            warnings.append(
                "HAND_TOO_SMALL"
            )

        # --------------------------------------------------
        # ACCEPTED
        # --------------------------------------------------

        print("Frame Accepted")

        print(
            "Visible Landmarks :",
            visible_landmarks
        )

        print(
            "Hand Width        :",
            round(width, 4)
        )

        print(
            "Hand Height       :",
            round(height, 4)
        )

        print(
            "Warnings          :",
            warnings
        )

        print("====================================")

        return self._result(
            valid=True,
            reason="VALID",
            hand_count=hand_count,
            person_count=person_count,
            body_visible=body_visible,
            landmark_count=len(landmarks),
            visible_landmarks=visible_landmarks,
            hand_width=width,
            hand_height=height,
            warnings=warnings
        )

    # ==================================================
    # RESULT
    # ==================================================

    def _result(
        self,
        valid,
        reason,
        hand_count=0,
        person_count=0,
        body_visible=False,
        landmark_count=0,
        visible_landmarks=0,
        hand_width=0.0,
        hand_height=0.0,
        warnings=None
    ):

        if warnings is None:

            warnings = []

        validation = {

            "valid": valid,

            "reason": reason,

            "hand_count": hand_count,

            "person_count": person_count,

            "body_visible": body_visible,

            "landmark_count": landmark_count,

            "visible_landmarks":
                visible_landmarks,

            "hand_width":
                round(
                    hand_width,
                    4
                ),

            "hand_height":
                round(
                    hand_height,
                    4
                ),

            "warnings":
                warnings
        }

        return {

            # Main detection result
            "valid": valid,

            "reason": reason,

            # IMPORTANT:
            # AssessmentService expects this key.
            "validation": validation,

            # Extra information
            "hand_count": hand_count,

            "person_count": person_count,

            "body_visible": body_visible,

            "landmark_count": landmark_count,

            "visible_landmarks":
                visible_landmarks,

            "hand_width":
                round(
                    hand_width,
                    4
                ),

            "hand_height":
                round(
                    hand_height,
                    4
                ),

            "warnings":
                warnings
        }