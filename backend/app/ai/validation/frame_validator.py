class FrameValidator:
    """
    SignSync Frame Validator

    Validates every webcam frame before gesture recognition.

    Returns
    -------
    {
        "valid": True / False,
        "reason": "<validation reason>"
    }

    Validation Reasons
    ------------------
    VALID
    NO_PERSON_DETECTED
    NO_HAND_DETECTED
    MULTIPLE_PEOPLE
    MULTIPLE_HANDS
    INVALID_LANDMARKS
    HAND_OUTSIDE_FRAME
    HAND_TOO_SMALL
    PARTIAL_HAND
    PARTIAL_BODY
    """

    def __init__(self):

        # --------------------------------------------------
        # Relaxed validation values for live webcam
        # --------------------------------------------------

        # Allow the hand much closer to the image borders
        self.edge_margin = 0.01

        # Allow smaller hands (camera farther away)
        self.minimum_hand_size = 0.03

        # Minimum visible landmarks
        self.minimum_visible_landmarks = 15

    # ==================================================
    # Validate Frame
    # ==================================================

    def validate(
        self,
        landmarks,
        hand_count=1,
        person_count=1,
        body_visible=True
    ):

        # ------------------------------------------
        # No Person
        # ------------------------------------------

        if person_count == 0:
            print("Frame Rejected -> NO_PERSON_DETECTED")
            return {
                "valid": False,
                "reason": "NO_PERSON_DETECTED"
            }

        # ------------------------------------------
        # Multiple People
        # ------------------------------------------

        if person_count > 1:
            print("Frame Rejected -> MULTIPLE_PEOPLE")
            return {
                "valid": False,
                "reason": "MULTIPLE_PEOPLE"
            }

        # ------------------------------------------
        # Partial Body
        # ------------------------------------------



        # ------------------------------------------
        # No Hand
        # ------------------------------------------

        if landmarks is None:
            print("Frame Rejected -> NO_HAND_DETECTED")
            return {
                "valid": False,
                "reason": "NO_HAND_DETECTED"
            }

        if len(landmarks) == 0:
            print("Frame Rejected -> NO_HAND_DETECTED")
            return {
                "valid": False,
                "reason": "NO_HAND_DETECTED"
            }

        # ------------------------------------------
        # Multiple Hands
        # ------------------------------------------

        if hand_count > 1:
            print("Frame Rejected -> MULTIPLE_HANDS")
            return {
                "valid": False,
                "reason": "MULTIPLE_HANDS"
            }

        # ------------------------------------------
        # Landmark Count
        # ------------------------------------------

        if len(landmarks) != 21:
            print(
                f"Frame Rejected -> INVALID_LANDMARKS ({len(landmarks)})"
            )
            return {
                "valid": False,
                "reason": "INVALID_LANDMARKS"
            }

        # ------------------------------------------
        # Count Visible Landmarks
        # ------------------------------------------

        visible = 0

        for point in landmarks:

            if (
                not isinstance(point, (list, tuple))
                or len(point) < 2
            ):
                continue

            x = point[0]
            y = point[1]

            if 0 <= x <= 1 and 0 <= y <= 1:
                visible += 1

        if visible < self.minimum_visible_landmarks:
            print(
                f"Frame Rejected -> PARTIAL_HAND ({visible}/21 visible)"
            )
            return {
                "valid": False,
                "reason": "PARTIAL_HAND"
            }

        # ------------------------------------------
        # Coordinates
        # ------------------------------------------

        try:

            xs = [p[0] for p in landmarks]
            ys = [p[1] for p in landmarks]

        except Exception:

            print("Frame Rejected -> INVALID_LANDMARKS")
            return {
                "valid": False,
                "reason": "INVALID_LANDMARKS"
            }

        # ------------------------------------------
        # Hand Outside Frame
        # (Warning only)
        # ------------------------------------------

        if (
            min(xs) < self.edge_margin
            or max(xs) > (1 - self.edge_margin)
            or min(ys) < self.edge_margin
            or max(ys) > (1 - self.edge_margin)
        ):
            print("Warning -> HAND_OUTSIDE_FRAME")
            # Do NOT reject

        # ------------------------------------------
        # Hand Size
        # (Warning only)
        # ------------------------------------------

        width = max(xs) - min(xs)
        height = max(ys) - min(ys)

        if (
            width < self.minimum_hand_size
            or height < self.minimum_hand_size
        ):
            print(
                f"Warning -> HAND_TOO_SMALL "
                f"(width={width:.3f}, height={height:.3f})"
            )
            # Do NOT reject

        # ------------------------------------------
        # Frame Accepted
        # ------------------------------------------

        print("Frame Accepted")

        return {
            "valid": True,
            "reason": "VALID"
        }