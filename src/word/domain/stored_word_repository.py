import abc
from typing import Optional
from src.word.domain.word import Word
from src.word.domain.stored_word import StoredWord
from src.word.domain.stored_word_factory import StoredWordFactory

class StoredWordRepository(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    async def find(
        self,
        word: Word,
    ) -> Optional[StoredWord]:
        raise NotImplementedError
    
    @abc.abstractmethod
    async def save(
        self,
        stored_word: StoredWord,
    ) -> StoredWord:
        raise NotImplementedError
