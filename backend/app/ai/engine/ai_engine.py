import time
import cv2
import numpy as np
import pandas as pd

from app.ai.hand_tracking.hand_detector import HandDetector
from app.ai.gesture_recognition.landmark_converter import LandmarkConverter
from app.ai.ml.inference.feature_converter import FeatureConverter
from app.ai.ml.preprocessing.feature_validator import FeatureValidator
from app.ai.ml.preprocessing.feature_normalizer import FeatureNormalizer

from app.ai.engine.model_manager import ModelManager
from app.ai.engine.prediction_result import PredictionResult
from app.ai.engine.inference_logger import InferenceLogger

from app.ai.ml.training.model_config import CONFIDENCE_THRESHOLD


class AIEngine:
    """
    Production-ready AI Engine.
    """

    def __init__(self):

        self.model_manager = ModelManager()

        self.logger = InferenceLogger()

        # LIVE CAMERA DETECTOR
        self.detector = HandDetector(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7,
        )

    # ===================================================
    # Predict using feature vector
    # ===================================================

    def predict(self, features):

        start = time.perf_counter()

        if not FeatureValidator.validate(features):
            return PredictionResult.failure(
                "Invalid feature vector."
            )

        features = FeatureNormalizer.normalize(
            features
        )

        feature_names = []

        for i in range(21):

            feature_names.extend(
                [
                    f"x{i}",
                    f"y{i}",
                    f"z{i}",
                ]
            )

        X = np.array(features).reshape(
            1,
            -1,
        )

        X = pd.DataFrame(
            X,
            columns=feature_names,
        )

        model = self.model_manager.model

        prediction = model.predict(X)[0]

        probabilities = model.predict_proba(X)[0]

        confidence = float(
            max(probabilities) * 100
        )

        inference_time = (
            time.perf_counter() - start
        ) * 1000

        if confidence < CONFIDENCE_THRESHOLD:

            self.logger.log(
                prediction="Unknown",
                confidence=confidence,
                model_version=self.model_manager.version,
                inference_time_ms=inference_time,
            )

            return PredictionResult.failure(
                f"Low confidence prediction ({confidence:.2f}%)."
            )

        self.logger.log(
            prediction=prediction,
            confidence=confidence,
            model_version=self.model_manager.version,
            inference_time_ms=inference_time,
        )

        return PredictionResult(
            prediction=prediction,
            confidence=confidence,
            model_version=self.model_manager.version,
            inference_time_ms=inference_time,
        )

    # ===================================================
    # Predict from image
    # ===================================================
    def predict_image(self, image):
        detection = self.detector.detect(image)
        frame = detection["frame"]
        hand_count = detection["hand_count"]
        hands = detection["landmarks"]
        print("\n==============================")
        print("AI ENGINE")
        print("Hand Count :", hand_count)
        print("==============================")
        if hand_count == 0:
            return PredictionResult.failure(
            "No hand detected."
        )
        if hand_count > 1:
            return PredictionResult.failure(
            "Multiple hands detected. Only one hand supported."
        )
        landmarks = LandmarkConverter.to_model_format(
        hands[0]
    )
        features = FeatureConverter.to_feature_vector(
        landmarks
    )
        result = self.predict(features)
        if result.success:result.landmarks = landmarks
        result.features = features
        return result

    # ===================================================
    # Predict from image path
    # ===================================================

    def predict_from_path(self, image_path):

        image = cv2.imread(image_path)

        if image is None:

            return PredictionResult.failure(
                "Unable to read image."
            )

        return self.predict_image(image)