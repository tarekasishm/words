from collections import Counter

from src.word.domain.anagram import Anagram
from src.word.domain.position import Position
from src.word.domain.stored_word import StoredWord
from src.word.domain.word import Word


class StoredWordFactory:
    @classmethod
    def build(
        cls,
        word: str,
        position: int,
    ) -> StoredWord:
        word_vo: Word = Word(word)
        position_vo: Position = Position(position)
        anagram: Anagram = Anagram(dict(Counter(sorted(word))))

        stored_word: StoredWord = StoredWord(
            word_vo,
            position_vo,
            anagram,
        )
        return stored_word
