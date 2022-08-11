import abc
from typing import List, Optional

from src.shared.domain.offset import Offset
from src.shared.domain.limit import Limit
from src.word.domain.word import Word
from src.word.domain.stored_word import StoredWord


class StoredWordRepository(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    async def find(
        self,
        word: Word,
    ) -> Optional[StoredWord]:
        raise NotImplementedError

    @abc.abstractmethod
    async def find_words(
        self,
        limit: Limit,
        offset: Offset,
    ) -> List[StoredWord]:
        raise NotImplementedError

    @abc.abstractmethod
    async def save(
        self,
        stored_word: StoredWord,
    ) -> StoredWord:
        raise NotImplementedError
