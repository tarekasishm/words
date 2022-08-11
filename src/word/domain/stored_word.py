from __future__ import annotations
from pydantic.dataclasses import dataclass
from collections import Counter

from src.word.domain.position import Position
from src.word.domain.word import Word


@dataclass
class StoredWord:
    def __init__(
        self,
        word: Word,
        position: Position,
    ) -> None:
        self.__word = word
        self.__position = position

    @property
    def word(self) -> str:
        return self.__word.word

    @property
    def position(self) -> int:
        return self.__position.position
