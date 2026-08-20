class FeatureValidator:
    """
    Validates extracted landmark features before prediction.
    Ensures the model always receives a valid 63-dimensional
    feature vector.
    """

    EXPECTED_FEATURES = 63

    @staticmethod
    def validate(features):
        """
        Validate feature vector.

        Parameters
        ----------
        features : list | tuple

        Returns
        -------
        bool
        """

        if features is None:
            return False

        if len(features) != FeatureValidator.EXPECTED_FEATURES:
            return False

        for value in features:

            if value is None:
                return False

            if not isinstance(value, (int, float)):
                return False

        return True