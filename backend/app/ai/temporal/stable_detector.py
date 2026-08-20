from collections import deque


class StableGestureDetector:
    """
    Determines when a gesture has remained consistent
    for the required number of frames.
    """

    def __init__(
        self,
        required_stable_frames=3,
        confidence_threshold=0.10,
        stability_threshold=60,
        history_size=5
    ):

        self.required_stable_frames = required_stable_frames
        self.confidence_threshold = confidence_threshold
        self.stability_threshold = stability_threshold
        self.history_size = history_size

        self.current_prediction = None
        self.current_confidences = []

        self.consecutive_frames = 0
        self.unstable_frames = 0

        self.last_stable_prediction = None
        self.new_stable_detected = False

        self.history = deque(
            maxlen=self.history_size
        )

    # ==================================================
    # RESET
    # ==================================================

    def reset(self):

        self.current_prediction = None
        self.current_confidences = []

        self.consecutive_frames = 0
        self.unstable_frames = 0

        self.last_stable_prediction = None
        self.new_stable_detected = False

        self.history.clear()

    # ==================================================
    # UPDATE
    # ==================================================

    def update(
        self,
        prediction,
        confidence
    ):

        print("\n========== STABLE DETECTOR UPDATE ==========")
        print("Detector ID:", id(self))
        print("Prediction received:", prediction)
        print("Confidence received:", confidence)
        print(
            "Consecutive BEFORE:",
            self.consecutive_frames
        )
        print(
            "Current prediction BEFORE:",
            self.current_prediction
        )

        self.new_stable_detected = False

        # --------------------------------------------------
        # Normalize prediction
        # --------------------------------------------------

        if prediction is None:

            return self._reset_response(
                reason="NONE_PREDICTION"
            )

        prediction = str(
            prediction
        ).strip().upper()

        if prediction in (
            "",
            "UNKNOWN",
            "NONE"
        ):

            return self._reset_response(
                reason="INVALID_PREDICTION"
            )

        # --------------------------------------------------
        # Normalize confidence
        # --------------------------------------------------

        try:

            confidence = float(
                confidence
            )

        except (
            TypeError,
            ValueError
        ):

            confidence = 0.0

        if confidence > 1:

            confidence /= 100.0

        confidence = max(
            0.0,
            min(
                confidence,
                1.0
            )
        )

        print(
            "Normalized confidence:",
            confidence
        )

        # --------------------------------------------------
        # Confidence filter
        # --------------------------------------------------

        if confidence < self.confidence_threshold:

            self.unstable_frames += 1

            print(
                "Rejected by confidence threshold"
            )

            return self._response(
                stable=False,
                prediction=None,
                confidence=confidence
            )

        # --------------------------------------------------
        # SAME PREDICTION
        # --------------------------------------------------

        if (
            self.current_prediction
            == prediction
        ):

            self.consecutive_frames += 1

            self.current_confidences.append(
                confidence
            )

            print(
                "Same prediction -> increment"
            )

        else:

            self.current_prediction = prediction

            self.consecutive_frames = 1

            self.current_confidences = [
                confidence
            ]

            print(
                "New prediction -> reset counter to 1"
            )

        # --------------------------------------------------
        # Add to history
        # --------------------------------------------------

        self.history.append(
            {
                "prediction": prediction,
                "confidence": confidence
            }
        )

        print(
            "History:",
            list(self.history)
        )

        print(
            "Consecutive AFTER:",
            self.consecutive_frames
        )

        # --------------------------------------------------
        # Average confidence
        # --------------------------------------------------

        average_confidence = (
            sum(
                self.current_confidences
            )
            /
            len(
                self.current_confidences
            )
        )

        # --------------------------------------------------
        # Majority vote
        # --------------------------------------------------

        counts = {}

        for item in self.history:

            p = item["prediction"]

            counts[p] = (
                counts.get(p, 0)
                + 1
            )

        majority_prediction = None
        majority_ratio = 0.0

        if counts:

            majority_prediction = max(
                counts,
                key=counts.get
            )

            majority_count = counts[
                majority_prediction
            ]

            majority_ratio = (
                majority_count
                /
                len(self.history)
            ) * 100

        # --------------------------------------------------
        # Frame stability
        # --------------------------------------------------

        frame_stability = min(
            (
                self.consecutive_frames
                /
                self.required_stable_frames
            ) * 100,
            100
        )

        # --------------------------------------------------
        # Gesture stability
        # --------------------------------------------------

        gesture_stability = min(
            frame_stability,
            majority_ratio
        )

        # --------------------------------------------------
        # Stable condition
        # --------------------------------------------------

        is_stable = (
            self.consecutive_frames
            >=
            self.required_stable_frames

            and

            average_confidence
            >=
            self.confidence_threshold

            and

            majority_ratio
            >=
            self.stability_threshold
        )

        print(
            "Average confidence:",
            average_confidence
        )

        print(
            "Majority prediction:",
            majority_prediction
        )

        print(
            "Majority ratio:",
            majority_ratio
        )

        print(
            "Frame stability:",
            frame_stability
        )

        print(
            "Gesture stability:",
            gesture_stability
        )

        print(
            "IS STABLE:",
            is_stable
        )

        # --------------------------------------------------
        # New stable gesture
        # --------------------------------------------------

        if is_stable:

            if (
                self.last_stable_prediction
                !=
                self.current_prediction
            ):

                self.new_stable_detected = True

            self.last_stable_prediction = (
                self.current_prediction
            )

            print(
                "***** STABLE GESTURE DETECTED *****"
            )

            return self._response(
                stable=True,
                prediction=self.current_prediction,
                confidence=average_confidence
            )

        # --------------------------------------------------
        # Not stable
        # --------------------------------------------------

        self.unstable_frames += 1

        return self._response(
            stable=False,
            prediction=None,
            confidence=average_confidence
        )

    # ==================================================
    # RESET RESPONSE
    # ==================================================

    def _reset_response(
        self,
        reason=""
    ):

        print(
            "Detector reset:",
            reason
        )

        self.current_prediction = None
        self.current_confidences = []
        self.consecutive_frames = 0

        return self._response(
            stable=False,
            prediction=None,
            confidence=0.0
        )

    # ==================================================
    # RESPONSE
    # ==================================================

    def _response(
        self,
        stable,
        prediction,
        confidence
    ):

        # --------------------------------------------------
        # Frame stability
        # --------------------------------------------------

        frame_stability = min(
            (
                self.consecutive_frames
                /
                self.required_stable_frames
            ) * 100,
            100
        )

        # --------------------------------------------------
        # Majority
        # --------------------------------------------------

        majority_prediction = None
        majority_ratio = 0.0

        if self.history:

            counts = {}

            for item in self.history:

                p = item["prediction"]

                counts[p] = (
                    counts.get(p, 0)
                    + 1
                )

            majority_prediction = max(
                counts,
                key=counts.get
            )

            majority_count = counts[
                majority_prediction
            ]

            majority_ratio = (
                majority_count
                /
                len(self.history)
            ) * 100

        # --------------------------------------------------
        # Gesture stability
        # --------------------------------------------------

        gesture_stability = min(
            frame_stability,
            majority_ratio
        )

        return {

            "stable":
                stable,

            "prediction":
                prediction,

            "confidence":
                round(
                    confidence,
                    3
                ),

            "stable_frames":
                self.consecutive_frames,

            "unstable_frames":
                self.unstable_frames,

            "required_frames":
                self.required_stable_frames,

            "gesture_stability":
                round(
                    gesture_stability,
                    2
                ),

            "majority_prediction":
                majority_prediction,

            "majority_ratio":
                round(
                    majority_ratio,
                    2
                ),

            "last_stable_prediction":
                self.last_stable_prediction,

            "new_stable":
                self.new_stable_detected
        }

    # ==================================================
    # STATUS
    # ==================================================

    def get_status(self):

        average_confidence = 0.0

        if self.current_confidences:

            average_confidence = (
                sum(
                    self.current_confidences
                )
                /
                len(
                    self.current_confidences
                )
            )

        return {

            "current_prediction":
                self.current_prediction,

            "last_stable_prediction":
                self.last_stable_prediction,

            "stable_frames":
                self.consecutive_frames,

            "required_frames":
                self.required_stable_frames,

            "average_confidence":
                round(
                    average_confidence,
                    3
                )
        }

    # ==================================================
    # HISTORY
    # ==================================================

    def get_history(self):

        return list(
            self.history
        )

    # ==================================================
    # LENGTH
    # ==================================================

    def __len__(self):

        return self.consecutive_frames