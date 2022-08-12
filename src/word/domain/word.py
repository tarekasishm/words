from pydantic import validator
from pydantic.dataclasses import dataclass
import re

from src.shared.domain.domain_exceptions import DomainException
from src.shared.domain.exceptions import INVALID_FIELD


@dataclass(frozen=True)
class Word:
    word: str

    @validator("word")
    def word_validator(
        cls,
        word: str,
    ) -> str:
        # electroencefalografista is longest word (23) in spanish
        pattern: str = r"^[a-zá-úüA-ZÁ-ÚÜ]{1,23}$"
        if not re.match(pattern, word):
            print(word)
            raise DomainException(
                "word",
                INVALID_FIELD,
                "Word does not follow the pattern",
            )
        return word
