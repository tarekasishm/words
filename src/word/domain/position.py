from __future__ import annotations
from typing import Union

from pydantic import validator
from pydantic.dataclasses import dataclass

from src.shared.domain.domain_exceptions import DomainException
from src.shared.domain.exceptions import CONFLICT, INVALID_FIELD


@dataclass(frozen=True)
class Position:
    position: int

    @validator("position")
    def position_validator(
        cls,
        position: int,
    ) -> int:
        if position < 1:
            raise DomainException(
                "Position", INVALID_FIELD, "Position must be a positive integer"
            )
        return position

    def __lt__(
        self,
        other: Position,
    ) -> bool:
        if not isinstance(other, Position):
            raise DomainException(
                "Position",
                INVALID_FIELD,
                "Position cannot be compared",
            )
        return self.position < other.position
