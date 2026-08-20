class FeatureNormalizer:
    """
    Normalizes a 63-dimensional landmark feature vector.

    Strategy:
    ----------
    Wrist-relative normalization.

    Landmark 0 (wrist) becomes the origin by subtracting its
    coordinates from every landmark.
    """

    @staticmethod
    def normalize(features):

        if features is None:
            return None

        if len(features) != 63:
            return None

        wrist_x = features[0]
        wrist_y = features[1]
        wrist_z = features[2]

        normalized = []

        for i in range(0, 63, 3):

            normalized.extend([
                features[i]     - wrist_x,
                features[i + 1] - wrist_y,
                features[i + 2] - wrist_z
            ])

        return normalized