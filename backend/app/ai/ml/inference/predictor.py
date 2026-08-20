from pathlib import Path
import time

import joblib
import numpy as np
import pandas as pd


# ==========================================================
# SignSync - Random Forest Predictor
# ==========================================================

BACKEND_ROOT = Path(__file__).resolve().parents[4]

MODEL_PATH = (
    BACKEND_ROOT
    / "app"
    / "ai"
    / "ml"
    / "models"
    / "random_forest.pkl"
)

LABEL_PATH = (
    BACKEND_ROOT
    / "app"
    / "ai"
    / "ml"
    / "models"
    / "label_names.pkl"
)


class Predictor:

    def __init__(self):

        if not MODEL_PATH.exists():
            raise FileNotFoundError(
                f"Random Forest model not found:\n{MODEL_PATH}"
            )

        if not LABEL_PATH.exists():
            raise FileNotFoundError(
                f"Label file not found:\n{LABEL_PATH}"
            )

        self.model = joblib.load(MODEL_PATH)

        self.labels = joblib.load(LABEL_PATH)

    # ======================================================
    # Normalize landmarks
    # ======================================================

    def normalize_landmarks(self, landmarks):

        landmarks = np.array(
            landmarks,
            dtype=np.float32
        )

        if landmarks.shape != (21, 3):
            raise ValueError(
                f"Expected (21,3) landmarks, got {landmarks.shape}"
            )

        wrist = landmarks[0]

        normalized = landmarks - wrist

        return normalized.flatten()

    # ======================================================
    # Feature Names
    # ======================================================

    def get_feature_names(self):

        names = []

        for i in range(21):

            names.extend([
                f"x{i}",
                f"y{i}",
                f"z{i}"
            ])

        return names

    # ======================================================
    # Prediction
    # ======================================================

    def predict(self, landmarks):

        start_time = time.perf_counter()

        if landmarks is None or len(landmarks) == 0:

            return {
                "prediction": "No hand detected",
                "confidence": 0.0,
                "confidence_percent": 0.0,
                "processing_time": 0.0
            }

        try:

            features = self.normalize_landmarks(
                landmarks
            )

            if len(features) != 63:
                raise ValueError(
                    "Feature length must be exactly 63."
                )

            dataframe = pd.DataFrame(
                features.reshape(1, -1),
                columns=self.get_feature_names()
            )

            prediction = str(
                self.model.predict(dataframe)[0]
            ).strip()

            confidence = 0.0

            if hasattr(self.model, "predict_proba"):

                probabilities = self.model.predict_proba(
                    dataframe
                )[0]

                confidence = float(
    np.max(probabilities)
)

                confidence = round(
    confidence,
    4
)
            confidence = max(
                0.0,
                min(confidence, 1.0)
            )

            processing_time = round(
                time.perf_counter() - start_time,
                4
            )

            return {

                "prediction": prediction,

                "confidence": confidence,

                "confidence_percent": round(
                    confidence * 100,
                    2
                ),

                "processing_time": processing_time

            }

        except Exception as error:

            print(
                "Prediction error:",
                error
            )

            return {

                "prediction": "Prediction failed",

                "confidence": 0.0,

                "confidence_percent": 0.0,

                "processing_time": round(
                    time.perf_counter() - start_time,
                    4
                )

            }