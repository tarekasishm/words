from typing import List

from src.shared.application.application_exceptions import (
    ApplicationException,
)
from src.shared.domain.domain_exceptions import DomainException
from ...shared.domain.offset import Offset
from ...shared.domain.limit import Limit
from src.word.application.words_dto import WordsDto
from ..domain.stored_word import StoredWord
from src.word.domain.stored_word_repository import (
    StoredWordRepository,
)


class GetWordsUseCase:
    def __init__(
        self,
        stored_word_repository: StoredWordRepository,
    ) -> None:
        self.__stored_word_repository = stored_word_repository

    async def get_words(
        self,
        limit: int,
        offset: int,
    ) -> WordsDto:
        try:
            stored_words: List[
                StoredWord
            ] = await self.__stored_word_repository.find_words(
                Limit(limit),
                Offset(offset),
            )
            words: List[str] = [stored_word.word for stored_word in stored_words]
            return WordsDto(data=words)
        except DomainException as domain_exception:
            raise ApplicationException(
                domain_exception.standard_exception,
                domain_exception.exception_message,
            )
