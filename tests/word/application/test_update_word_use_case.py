import pytest

from src.shared.application.application_exceptions import ApplicationException
from src.shared.domain.exceptions import NOT_FOUND
from src.word.application.update_word_use_case import (
    UpdateWordUseCase,
)
from src.word.application.stored_word_dto import StoredWordDto
from tests.word.application.stored_word_mock_repository import (
    StoredWordMockRepository,
)


class TestUpdateWordUseCase:
    @pytest.mark.asyncio
    async def test_update_word_success(self) -> None:
        stored_word_repository: StoredWordMockRepository = StoredWordMockRepository()
        update_word_use_case: UpdateWordUseCase = UpdateWordUseCase(
            stored_word_repository,
        )

        response: StoredWordDto = await update_word_use_case.update(
            "pepe",
            8,
        )
        expected_response: StoredWordDto = StoredWordDto(word="pepe", position=8)

        assert response == expected_response

    @pytest.mark.asyncio
    async def test_update_non_stored_word(self) -> None:
        stored_word_repository: StoredWordMockRepository = StoredWordMockRepository()
        update_word_use_case: UpdateWordUseCase = UpdateWordUseCase(
            stored_word_repository,
        )
        with pytest.raises(ApplicationException) as application_exception:
            await update_word_use_case.update(
                "calabozo",
                8,
            )
        assert application_exception.value.exception_message == "calabozo not found"
        assert application_exception.value.standard_exception == NOT_FOUND
