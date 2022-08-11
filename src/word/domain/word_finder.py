from typing import Optional

from src.word.domain.stored_word import StoredWord
from src.word.domain.stored_word_repository import StoredWordRepository
from src.word.domain.word import Word
from src.shared.domain.domain_exceptions import DomainException
from src.shared.domain.exceptions import CONFLICT


class WordFinder:
    def __init__(
        self,
        stored_word_repository: StoredWordRepository,
    ) -> None:
        self.__stored_word_repository = stored_word_repository

    async def find(
        self,
        word: Word,
    ) -> None:
        stored_word: Optional[StoredWord] = await self.__stored_word_repository.find(
            word,
        )
        if stored_word is not None:
            raise DomainException("WordFinder", CONFLICT, f"{word.word} already exists")
