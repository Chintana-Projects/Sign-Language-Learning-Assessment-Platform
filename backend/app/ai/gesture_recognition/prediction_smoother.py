from collections import Counter, deque


class PredictionSmoother:

    def __init__(
        self,
        window_size=15,
        confidence_threshold=0.40,
        min_votes=3,
        min_vote_ratio=0.50,
        switch_consecutive=3
    ):
        self.window_size = window_size
        self.confidence_threshold = confidence_threshold
        self.min_votes = min_votes
        self.min_vote_ratio = min_vote_ratio
        self.switch_consecutive = switch_consecutive

        self.predictions = deque(maxlen=window_size)

        # Currently stable gesture
        self.current_prediction = None

        # Used to detect a new gesture
        self.candidate_prediction = None
        self.candidate_count = 0

    # ------------------------------------------------------
    # Add prediction
    # ------------------------------------------------------

    def add_prediction(self, prediction, confidence):

        # Ignore invalid prediction
        if prediction is None:
            return self.get_stable_prediction()

        confidence = float(confidence)

        # Ignore weak prediction
        if confidence < self.confidence_threshold:
            return self.get_stable_prediction()

        # Store prediction
        self.predictions.append({
            "prediction": prediction,
            "confidence": confidence
        })

        # --------------------------------------------------
        # No stable gesture yet
        # --------------------------------------------------

        if self.current_prediction is None:

            result = self._calculate_window_prediction()

            if result["prediction"] != "Uncertain":
                self.current_prediction = result["prediction"]

            return result

        # --------------------------------------------------
        # Same gesture
        # --------------------------------------------------

        if prediction == self.current_prediction:

            self.candidate_prediction = None
            self.candidate_count = 0

            return self._calculate_current_prediction()

        # --------------------------------------------------
        # New gesture candidate
        # --------------------------------------------------

        if prediction == self.candidate_prediction:

            self.candidate_count += 1

        else:

            self.candidate_prediction = prediction
            self.candidate_count = 1

        # --------------------------------------------------
        # Strong consecutive new gesture
        # --------------------------------------------------

        if self.candidate_count >= self.switch_consecutive:

            self.current_prediction = self.candidate_prediction

            self.candidate_prediction = None
            self.candidate_count = 0

            return self._calculate_current_prediction()

        # Keep current stable gesture
        return self._calculate_current_prediction()

    # ------------------------------------------------------
    # Calculate window prediction
    # ------------------------------------------------------

    def _calculate_window_prediction(self):

        if not self.predictions:
            return {
                "prediction": "Uncertain",
                "confidence": 0.0,
                "votes": 0,
                "window_size": 0
            }

        counts = Counter(
            item["prediction"]
            for item in self.predictions
        )

        prediction, vote_count = counts.most_common(1)[0]

        total = len(self.predictions)

        vote_ratio = vote_count / total

        # Need minimum votes
        if vote_count < self.min_votes:

            return {
                "prediction": "Uncertain",
                "confidence": 0.0,
                "votes": vote_count,
                "window_size": total
            }

        # Need sufficient agreement
        if vote_ratio < self.min_vote_ratio:

            return {
                "prediction": "Uncertain",
                "confidence": 0.0,
                "votes": vote_count,
                "window_size": total
            }

        matching_confidences = [
            item["confidence"]
            for item in self.predictions
            if item["prediction"] == prediction
        ]

        average_confidence = (
            sum(matching_confidences)
            / len(matching_confidences)
        )

        return {
            "prediction": prediction,
            "confidence": average_confidence,
            "votes": vote_count,
            "window_size": total
        }

    # ------------------------------------------------------
    # Calculate current stable prediction
    # ------------------------------------------------------

    def _calculate_current_prediction(self):

        matching = [
            item
            for item in self.predictions
            if item["prediction"] == self.current_prediction
        ]

        if not matching:

            return {
                "prediction": self.current_prediction,
                "confidence": 0.0,
                "votes": 0,
                "window_size": len(self.predictions)
            }

        average_confidence = (
            sum(item["confidence"] for item in matching)
            / len(matching)
        )

        return {
            "prediction": self.current_prediction,
            "confidence": average_confidence,
            "votes": len(matching),
            "window_size": len(self.predictions)
        }

    # ------------------------------------------------------
    # Public stable prediction
    # ------------------------------------------------------

    def get_stable_prediction(self):

        if self.current_prediction is None:
            return self._calculate_window_prediction()

        return self._calculate_current_prediction()

    # ------------------------------------------------------
    # Reset
    # ------------------------------------------------------

    def reset(self):

        self.predictions.clear()

        self.current_prediction = None

        self.candidate_prediction = None
        self.candidate_count = 0