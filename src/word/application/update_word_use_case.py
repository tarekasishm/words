from typing import Optional
from src.shared.application.application_exceptions import (
    ApplicationException,
)
from src.shared.domain.domain_exceptions import DomainException
from src.word.domain.stored_word_factory import StoredWordFactory
from src.shared.domain.exceptions import NOT_FOUND
from src.word.application.stored_word_dto import StoredWordDto
from src.word.domain.stored_word import StoredWord
from src.word.domain.stored_word_repository import StoredWordRepository
from src.word.domain.word import Word


class UpdateWordUseCase:
    def __init__(
        self,
        stored_word_repository: StoredWordRepository,
    ) -> None:
        self.__stored_word_repository = stored_word_repository

    async def update(
        self,
        word: str,
        new_position: int,
    ) -> StoredWordDto:
        try:
            word_vo: Word = Word(word)
            current_stored_word: Optional[
                StoredWord
            ] = await self.__stored_word_repository.find(word_vo)
            if current_stored_word is None:
                raise ApplicationException(
                    NOT_FOUND,
                    f"{word_vo.word} not found",
                )
            updated_word: StoredWord = StoredWordFactory.build(
                word_vo.word, new_position
            )
            updated_word = await self.__stored_word_repository.update(
                updated_word,
            )
            return StoredWordDto(
                word=updated_word.word,
                position=updated_word.position,
            )
        except (DomainException, ApplicationException) as exception:
            raise ApplicationException(
                exception.standard_exception,
                exception.exception_message,
            )
