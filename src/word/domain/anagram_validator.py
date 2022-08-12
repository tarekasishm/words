from collections import Counter

from src.word.domain.word import Word


class AnagramValidator:
    @classmethod
    def is_anagram(
        cls,
        left_word: Word,
        right_word: Word,
    ) -> bool:
        self_frequency: Counter[str] = Counter(left_word.word)
        other_frequency: Counter[str] = Counter(right_word.word)

        return self_frequency == other_frequency and left_word.word != right_word.word
