class FingerStateDetector:
    """
    Detects whether each finger is
    Extended or Bent.

    MediaPipe Landmark Indexes

    Thumb:
        2 MCP
        3 IP
        4 Tip

    Index:
        5 MCP
        6 PIP
        8 Tip

    Middle:
        9 MCP
        10 PIP
        12 Tip

    Ring:
        13 MCP
        14 PIP
        16 Tip

    Little:
        17 MCP
        18 PIP
        20 Tip
    """

    @staticmethod
    def detect(landmarks):

        if landmarks is None or len(landmarks) != 21:
            return {}

        fingers = {}

        # -----------------------------
        # Thumb
        # -----------------------------

        thumb_tip = landmarks[4]
        thumb_ip = landmarks[3]

        fingers["thumb"] = (
            "extended"
            if thumb_tip[0] > thumb_ip[0]
            else "bent"
        )

        # -----------------------------
        # Index
        # -----------------------------

        fingers["index"] = (
            "extended"
            if landmarks[8][1] < landmarks[6][1]
            else "bent"
        )

        # -----------------------------
        # Middle
        # -----------------------------

        fingers["middle"] = (
            "extended"
            if landmarks[12][1] < landmarks[10][1]
            else "bent"
        )

        # -----------------------------
        # Ring
        # -----------------------------

        fingers["ring"] = (
            "extended"
            if landmarks[16][1] < landmarks[14][1]
            else "bent"
        )

        # -----------------------------
        # Little
        # -----------------------------

        fingers["little"] = (
            "extended"
            if landmarks[20][1] < landmarks[18][1]
            else "bent"
        )

        return fingers