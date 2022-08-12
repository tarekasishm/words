from src.word.domain.anagram_validator import AnagramValidator
from src.word.domain.word import Word


class TestAnagramValidator:
    def test_valid_anagram(self) -> None:
        w1: Word = Word("quieren")
        w2: Word = Word("enrique")

        assert AnagramValidator.is_anagram(w1, w2)

    def test_invalid_anagram(self) -> None:
        w1: Word = Word("quieren")
        w2: Word = Word("enriq")

        assert not AnagramValidator.is_anagram(w1, w2)
