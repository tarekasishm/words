from src.shared.application.application_exceptions import (
    ApplicationException,
)
from src.shared.domain.domain_exceptions import DomainException
from src.word.domain.stored_word_repository import (
    StoredWordRepository,
)
from ..domain.word import Word


class DeleteWordUseCase:
    def __init__(
        self,
        stored_word_repository: StoredWordRepository,
    ) -> None:
        self.__stored_word_repository = stored_word_repository

    async def delete(
        self,
        word: str,
    ) -> None:
        try:
            await self.__stored_word_repository.delete(Word(word))
        except DomainException as domain_exception:
            raise ApplicationException(
                domain_exception.standard_exception,
                domain_exception.exception_message,
            )
