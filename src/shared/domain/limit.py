from pydantic.dataclasses import dataclass
from pydantic import validator

from src.shared.domain.domain_exceptions import DomainException
from src.shared.domain.exceptions import INVALID_FIELD


@dataclass(frozen=True)
class Limit:
    limit: int

    @validator("limit")
    def limit_validator(
        cls,
        limit: int,
    ) -> int:
        if limit <= 0:
            raise DomainException(
                "Limit",
                INVALID_FIELD,
                "Limit must a positive integer",
            )
        return limit
