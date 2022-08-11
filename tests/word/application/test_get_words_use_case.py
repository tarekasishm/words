import pytest

from src.word.application.get_words_use_case import (
    GetWordsUseCase,
)
from src.word.application.words_dto import WordsDto
from tests.word.application.stored_word_mock_repository import (
    StoredWordMockRepository,
)


class TestGetWordsUseCase:
    @pytest.mark.asyncio
    async def test_get_words_success(
        self,
    ) -> None:
        stored_word_repository: StoredWordMockRepository = StoredWordMockRepository()
        get_words_use_case: GetWordsUseCase = GetWordsUseCase(
            stored_word_repository,
        )

        response: WordsDto = await get_words_use_case.get_words(5, 0)
        expected_response: WordsDto = WordsDto(
            data=[
                "cosa",
                "caso",
                "calle",
                "paco",
                "pepe",
            ]
        )
        assert response == expected_response
