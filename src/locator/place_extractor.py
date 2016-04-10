class PlaceExtractor:

    def __init__(self, tweet):
        self.tweet = tweet

    @staticmethod
    def starts_with_capital_letter(word):
        return word[0] == word[0].upper()

    @staticmethod
    def is_too_short(word):
        return len(word) < 2

    @staticmethod
    def contains_number(word):
        return any(letter.isdigit() for letter in word)

    @staticmethod
    def remove_short_words(words):
        return [word for word in words \
            if not PlaceExtractor.is_too_short(word)]

    @staticmethod
    def ends_with_symbol(word):
        last_character = word[-1::]
        return not last_character.isalnum()

    @staticmethod
    def has_only_capital_letters(word):
        return word.upper() == word

    @classmethod
    def separate_words_divided_by_slash(cls, text):
        return text.replace('/', ' ')

    @classmethod
    def remove_words_with_only_capital_letters(cls, words):
        return [word for word in words \
            if not cls.has_only_capital_letters(word)]

    @classmethod
    def remove_trailing_symbol(cls, word):
        while cls.ends_with_symbol(word):
            word = word[:-1:]
        return word

    @classmethod
    def remove_words_with_numbers(cls, words):
        return [word for word in words \
            if not cls.contains_number(word)]

    @classmethod
    def remove_trailing_symbols(cls, words):
        return [cls.remove_trailing_symbol(word) \
            for word in words]

    @classmethod
    def find_words_with_capital_letter(cls, text):
        words = text.split(' ')
        return [word for word in words \
            if cls.starts_with_capital_letter(word)]

    @classmethod
    def remove_duplicate_words(cls, words):
        return list(set(words))

    def find_potential_places(self):
        text  = self.tweet.content
        text  = self.separate_words_divided_by_slash(text)
        words = self.find_words_with_capital_letter(text)
        words = self.remove_words_with_numbers(words)
        words = self.remove_words_with_only_capital_letters(words)
        words = self.remove_short_words(words)
        words = self.remove_trailing_symbols(words)
        words = self.remove_duplicate_words(words)
        return sorted(words)
