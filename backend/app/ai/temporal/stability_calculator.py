class StabilityCalculator:
    """
    SignSync Gesture Stability Calculator

    Calculates:
    - Gesture stability percentage
    - Prediction consistency
    - Stable confidence
    - Unstable frame count

    Compatible with:
    - Random Forest
    - LSTM
    - GRU
    - Transformer
    """

    def __init__(self):

        self.total_frames = 0

        self.valid_frames = 0

        self.stable_frames = 0

        self.unstable_frames = 0

        self.prediction_history = []

        self.confidence_history = []

        self.last_prediction = None



    # =================================================
    # Update Frame Stability
    # =================================================

    def update(
            self,
            prediction,
            confidence,
            stable=False
    ):
        """
        Update stability information.

        Parameters:
        prediction -> predicted gesture
        confidence -> model confidence
        stable -> StableGestureDetector result
        """

        self.total_frames += 1


        # -----------------------------
        # Invalid prediction
        # -----------------------------

        if prediction is None:

            self.unstable_frames += 1

            return self.get_metrics()



        prediction = str(
            prediction
        ).upper()


        confidence = float(
            confidence
        )


        if confidence > 1:

            confidence /= 100



        self.valid_frames += 1


        self.prediction_history.append(
            prediction
        )


        self.confidence_history.append(
            confidence
        )



        # -----------------------------
        # Stability tracking
        # -----------------------------

        if stable:

            self.stable_frames += 1


        else:

            self.unstable_frames += 1



        self.last_prediction = prediction



        return self.get_metrics()



    # =================================================
    # Calculate Stability
    # =================================================

    def calculate_stability(self):

        if self.total_frames == 0:

            return 0



        stability = (

            self.stable_frames

            /

            self.total_frames

        ) * 100


        return round(
            stability,
            2
        )



    # =================================================
    # Prediction Consistency
    # =================================================

    def calculate_consistency(self):

        if len(self.prediction_history) == 0:

            return 0



        if len(self.prediction_history) == 1:

            return 100



        latest = self.prediction_history[-1]


        same_count = sum(

            1

            for prediction in self.prediction_history

            if prediction == latest

        )


        consistency = (

            same_count

            /

            len(self.prediction_history)

        ) * 100



        return round(
            consistency,
            2
        )



    # =================================================
    # Stable Confidence
    # =================================================

    def calculate_confidence(self):

        if not self.confidence_history:

            return 0



        confidence = sum(

            self.confidence_history

        ) / len(
            self.confidence_history
        )


        return round(
            confidence,
            3
        )



    # =================================================
    # Metrics
    # =================================================

    def get_metrics(self):

        return {

            "gesture_stability":

                self.calculate_stability(),


            "prediction_consistency":

                self.calculate_consistency(),


            "stable_confidence":

                self.calculate_confidence(),


            "total_frames":

                self.total_frames,


            "valid_frames":

                self.valid_frames,


            "stable_frames":

                self.stable_frames,


            "unstable_frames":

                self.unstable_frames,


            "last_prediction":

                self.last_prediction

        }



    # =================================================
    # Reset
    # =================================================

    def reset(self):

        self.total_frames = 0

        self.valid_frames = 0

        self.stable_frames = 0

        self.unstable_frames = 0

        self.prediction_history.clear()

        self.confidence_history.clear()

        self.last_prediction = None