from src.shared.application.application_exceptions import ApplicationException
from src.shared.domain.domain_exceptions import DomainException
from src.word.application.stored_word_dto import StoredWordDto
from src.word.domain.stored_word import StoredWord
from src.word.domain.stored_word_factory import StoredWordFactory
from src.word.domain.stored_word_repository import StoredWordRepository


class CreateWordUseCase:
    def __init__(
        self,
        stored_word_repository: StoredWordRepository,
    ) -> None:
        self.__stored_word_repository = stored_word_repository

    async def create(
        self,
        word_dto: StoredWordDto,
    ) -> StoredWordDto:
        try:
            stored_word: StoredWord = StoredWordFactory.build(
                word_dto.word,
                word_dto.position,
            )
            await self.__stored_word_repository.save(
                stored_word,
            )
            return StoredWordDto(
                word=stored_word.word,
                position=stored_word.position,
            )

        except DomainException as domain_exception:
            raise ApplicationException(
                domain_exception.standard_exception,
                domain_exception.exception_message,
            )
