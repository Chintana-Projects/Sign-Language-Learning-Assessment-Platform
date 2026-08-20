from pathlib import Path
import joblib


class ModelManager:
    """
    Responsible for loading and managing ML models.

    Other parts of the application should never directly
    load model files.
    """

    def __init__(self):

        self.models_directory = (
            Path(__file__).resolve().parents[1]
            / "ml"
            / "models"
        )

        self.model_path = (
            self.models_directory
            / "random_forest.pkl"
        )

        self.labels_path = (
            self.models_directory
            / "label_names.pkl"
        )

        self.model_version = "RF_v1.0"

        self._model = None
        self._labels = None

    # ----------------------------------------
    # Load model only once
    # ----------------------------------------

    def load(self):

        if self._model is None:

            self._model = joblib.load(
                self.model_path
            )

            self._labels = joblib.load(
                self.labels_path
            )

        return self._model

    # ----------------------------------------
    # Get loaded model
    # ----------------------------------------

    @property
    def model(self):

        return self.load()

    # ----------------------------------------
    # Labels
    # ----------------------------------------

    @property
    def labels(self):

        if self._labels is None:
            self.load()

        return self._labels

    # ----------------------------------------
    # Version
    # ----------------------------------------

    @property
    def version(self):

        return self.model_version