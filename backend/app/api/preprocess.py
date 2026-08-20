from fastapi import APIRouter, HTTPException

from app.services.preprocessing_service import PreprocessingService


router = APIRouter(
    prefix="/preprocess",
    tags=["Preprocessing"]
)

preprocessing_service = PreprocessingService()


@router.post("")
def preprocess_dataset():

    try:
        result = preprocessing_service.preprocess()

        return result

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )