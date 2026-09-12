from pydantic import BaseModel


class LessonCreate(BaseModel):

    title: str
    description: str
    category: str

    sign: str | None = None
    image_url: str | None = None
    video_url: str | None = None