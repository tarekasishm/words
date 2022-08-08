from src.word.application.stored_word_dto import StoredWordDto
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
        pass