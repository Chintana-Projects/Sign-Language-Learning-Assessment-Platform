from fastapi import APIRouter
from app.services.gesture_service import GestureService
from app.schemas.prediction import PredictionResponse
from app.schemas.landmarks import LandmarkRequest

router = APIRouter()

gesture_service = GestureService()


@router.post("/predict", response_model=PredictionResponse)
def predict(request: LandmarkRequest):
    return gesture_service.predict(request.landmarks)