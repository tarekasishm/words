from typing import Any, Dict, List, Optional

from src.shared.domain.limit import Limit
from src.shared.domain.offset import Offset
from src.word.domain.stored_word import StoredWord
from src.word.domain.stored_word_factory import StoredWordFactory
from src.word.domain.stored_word_repository import StoredWordRepository
from src.word.domain.word import Word
from tests.word.application.fake_stored_words import fake_words


class StoredWordMockRepository(StoredWordRepository):
    async def find(
        self,
        word: Word,
    ) -> Optional[StoredWord]:
        fake_word: List[Dict[str, Any]] = [
            fake_word for fake_word in fake_words if fake_word["word"] == word.word
        ]
        if len(fake_word) == 0:
            return None
        stored_word: StoredWord = StoredWordFactory.build(
            fake_word[0]["word"], fake_word[0]["position"]
        )
        return stored_word

    async def find_words(
        self,
        limit: Limit,
        offset: Offset,
    ) -> List[StoredWord]:
        stored_words: List[StoredWord] = [
            StoredWordFactory.build(
                fake_word["word"],
                fake_word["position"],
            )
            for fake_word in fake_words[offset.offset : (offset.offset + limit.limit)]
        ]
        return stored_words

    async def save(
        self,
        stored_word: StoredWord,
    ) -> StoredWord:
        return stored_word

    async def update(
        self,
        stored_word: StoredWord,
    ) -> StoredWord:
        return stored_word

    async def delete(
        self,
        word: Word,
    ) -> None:
        pass

    async def find_anagrams(
        self,
        word: Word,
    ) -> List[StoredWord]:
        pass
