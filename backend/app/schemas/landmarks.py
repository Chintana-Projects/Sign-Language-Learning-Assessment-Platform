from typing import List, Optional, Dict, Any

from pydantic import BaseModel, Field, field_validator


class LandmarkRequest(BaseModel):

    landmarks: Optional[List[List[float]]] = Field(
        default=None
    )


    hand_count: int = Field(
        default=0,
        ge=0
    )


    person_count: int = Field(
        default=0,
        ge=0
    )


    body_visible: bool = Field(
        default=False
    )


    # NEW
    stable_prediction: Optional[Dict[str, Any]] = Field(
        default={}
    )


    # NEW
    motion_metrics: Optional[Dict[str, Any]] = Field(
        default={}
    )



    @field_validator("landmarks")
    @classmethod
    def validate_landmarks(cls, value):

        if value is None:
            return None


        if value == []:
            return []


        if len(value) != 21:
            raise ValueError(
                "Landmarks must contain exactly 21 points"
            )


        for point in value:

            if len(point) != 3:
                raise ValueError(
                    "Each landmark must contain x,y,z"
                )


            for coordinate in point:

                if not isinstance(
                    coordinate,
                    (int,float)
                ):
                    raise ValueError(
                        "Coordinates must be numeric"
                    )


        return value