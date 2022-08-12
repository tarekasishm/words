from pydantic import BaseModel


class WordPositionDto(BaseModel):
    position: int
