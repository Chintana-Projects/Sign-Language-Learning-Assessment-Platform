from dataclasses import dataclass, asdict, field
from typing import Optional, List
from datetime import datetime


@dataclass
class PredictionResult:
    """
    Standard prediction object returned by the AI Engine.

    This class hides all internal ML implementation details from
    the rest of the application.

    Additional optional fields (landmarks/features) are used only
    for temporal processing and do NOT affect prediction.
    """

    # -----------------------------
    # Prediction
    # -----------------------------
    prediction: str
    confidence: float
    model_version: str
    inference_time_ms: float

    # -----------------------------
    # Status
    # -----------------------------
    success: bool = True
    message: str = "Prediction completed successfully."

    # -----------------------------
    # Timestamp
    # -----------------------------
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

    # -----------------------------
    # Optional Temporal Data
    # -----------------------------
    landmarks: Optional[List] = None
    features: Optional[List[float]] = None

    # -----------------------------
    # Convert to dictionary
    # -----------------------------
    def to_dict(self):
        return asdict(self)

    # -----------------------------
    # Failure object
    # -----------------------------
    @classmethod
    def failure(cls, message):
        return cls(
            prediction="Unknown",
            confidence=0.0,
            model_version="N/A",
            inference_time_ms=0.0,
            success=False,
            message=message,
            landmarks=None,
            features=None
        )