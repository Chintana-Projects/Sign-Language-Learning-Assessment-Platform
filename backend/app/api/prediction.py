from fastapi import APIRouter, HTTPException

from app.services.gesture_service import GestureService
from app.schemas.landmarks import LandmarkRequest


router = APIRouter(
    prefix="/predict",
    tags=["Prediction"]
)


gesture_service = GestureService()



@router.post("/live")
def live_prediction(
        request: LandmarkRequest
):


    try:

        result = gesture_service.predict(
            request.landmarks
        )


        return {

            "success": True,

            "prediction":
                result.get(
                    "prediction",
                    "Unknown"
                ),

            "confidence":
                result.get(
                    "confidence",
                    0
                ),

            "inference_time":
                result.get(
                    "processing_time",
                    0
                )

        }


    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )