from src.word.domain.anagram_validator import AnagramValidator
from src.word.domain.stored_word import StoredWord
from src.word.domain.stored_word_factory import StoredWordFactory


class TestAnagramValidator:
    def test_valid_anagram(self) -> None:
        w1: StoredWord = StoredWordFactory.build(
            "quieren",
            3,
        )
        w2: StoredWord = StoredWordFactory.build(
            "enrique",
            5,
        )

        assert AnagramValidator.is_anagram(w1, w2)

    def test_invalid_anagram(self) -> None:
        w1: StoredWord = StoredWordFactory.build(
            "quieren",
            3,
        )
        w2: StoredWord = StoredWordFactory.build(
            "enriq",
            5,
        )

        assert not AnagramValidator.is_anagram(w1, w2)
