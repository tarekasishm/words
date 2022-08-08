from collections import Counter

from src.word.domain.stored_word import StoredWord

class AnagramValidator:

    @classmethod
    def is_anagram(
        cls,
        left_word: StoredWord,
        right_word: StoredWord,
    ) -> bool:
        self_frequency: Counter = Counter(left_word.word)
        other_frequency: Counter = Counter(right_word.word)

        return self_frequency == other_frequency and left_word.word != right_word.word
