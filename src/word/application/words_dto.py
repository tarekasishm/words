from typing import List
from pydantic import BaseModel


class WordsDto(BaseModel):
    data: List[str]
