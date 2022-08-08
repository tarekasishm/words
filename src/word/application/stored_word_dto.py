from pydantic import BaseModel

class StoredWordDto(BaseModel):
    word: str
    position: int