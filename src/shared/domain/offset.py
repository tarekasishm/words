from pydantic.dataclasses import dataclass
from pydantic import validator

from src.shared.domain.domain_exceptions import DomainException
from src.shared.domain.exceptions import INVALID_FIELD


@dataclass(frozen=True)
class Offset:
    offset: int

    @validator("offset")
    def offset_validator(
        cls,
        offset: int,
    ) -> int:
        if offset < 0:
            raise DomainException(
                "Offset",
                INVALID_FIELD,
                "Offset must greater than or equal to zero",
            )
        return offset
