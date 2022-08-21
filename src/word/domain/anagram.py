from typing import Dict

from pydantic import validator
from pydantic.dataclasses import dataclass

@dataclass(frozen=True)
class Anagram:
    anagram: Dict[str, int]
