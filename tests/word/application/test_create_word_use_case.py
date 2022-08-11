import pytest
from src.shared.application.application_exceptions import ApplicationException

from src.word.application.create_word_use_case import CreateWordUseCase
from src.word.application.stored_word_dto import StoredWordDto
from tests.word.application.stored_word_mock_repository import StoredWordMockRepository


class TestCreateWorduseCase:
    @pytest.mark.asyncio
    async def test_create_new_word(self) -> None:
        stored_word_repository: StoredWordMockRepository = StoredWordMockRepository()
        create_word_use_case: CreateWordUseCase = CreateWordUseCase(
            stored_word_repository,
        )

        create_word_dto: StoredWordDto = StoredWordDto(word="palabra", position=5)
        create_word_response_dto: StoredWordDto = await create_word_use_case.create(
            create_word_dto
        )

        expected_response: StoredWordDto = StoredWordDto(
            word="palabra",
            position=5,
        )
        assert create_word_response_dto == expected_response

    @pytest.mark.asyncio
    async def test_create_existing_word_exception(self) -> None:
        stored_word_repository: StoredWordMockRepository = StoredWordMockRepository()
        create_word_use_case: CreateWordUseCase = CreateWordUseCase(
            stored_word_repository,
        )

        create_word_dto: StoredWordDto = StoredWordDto(word="paco", position=5)
        with pytest.raises(ApplicationException) as application_exception:
            await create_word_use_case.create(create_word_dto)
        assert application_exception.value.exception_message == "paco already exists"
