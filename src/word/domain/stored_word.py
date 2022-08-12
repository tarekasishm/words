from __future__ import annotations
from pydantic.dataclasses import dataclass

from src.shared.domain.domain_exceptions import (
    DomainException,
)
from src.shared.domain.exceptions import CONFLICT
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

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, StoredWord):
            raise DomainException(
                "StoredWord",
                CONFLICT,
                "StoredWord can only compared with other instances of StoredWord",
            )
        return self.word == other.word and self.position == other.position
