from typing import List

from src.shared.application.application_exceptions import (
    ApplicationException,
)
from src.shared.domain.domain_exceptions import (
    DomainException,
)
from src.word.application.words_dto import WordsDto
from src.word.domain.stored_word import StoredWord
from src.word.domain.stored_word_repository import (
    StoredWordRepository,
)
from src.word.domain.word import Word


class GetAnagramsUseCase:
    def __init__(
        self,
        stored_word_repository: StoredWordRepository,
    ) -> None:
        self.__stored_word_repository = stored_word_repository

    async def get(
        self,
        word: str,
    ) -> WordsDto:
        try:
            anagrams: List[StoredWord] = await self.__stored_word_repository.find_anagrams(
                Word(word)
            )

            anagrams_str: List[str] = [anagram.word for anagram in anagrams]
            return WordsDto(data=anagrams_str)
        except DomainException as domain_exception:
            raise ApplicationException(
                domain_exception.standard_exception,
                domain_exception.exception_message,
            )