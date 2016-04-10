from .stopwords import stopwords

class PlaceExtractor:

    def __init__(self, tweet):
        self.tweet = tweet

    @staticmethod
    def starts_with_capital_letter(word):
        return word[0] == word[0].upper() if word else False

    @staticmethod
    def is_a_stopword(word):
        return word.lower() in stopwords

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
    def remove_hashtags_and_at_sign(cls, text):
        return text.replace('@', '').replace('#', '')

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
    def remove_stopwords(cls, words):
        return [word for word in words \
            if not cls.is_a_stopword(word)]

    @classmethod
    def find_words_with_capital_letter(cls, text):
        words = text.split(' ')
        return [word for word in words \
            if cls.starts_with_capital_letter(word)]

    @classmethod
    def remove_duplicate_words(cls, words):
        return list(set(words))

    def merge_words_that_are_next_to_each_other(self, places):
        text = self.tweet.content

        def get_neighbor(place, places):
            try:
                return places[places.index(place) + 1]
            except IndexError:
                return None

        def merge(text, places):
            for index, place in enumerate(places):
                neighbor = get_neighbor(place, places)
                
                if neighbor and (place + ' ' + neighbor) in text:
                    places[index] = place + ' ' + neighbor
                    places.remove(neighbor)
            return places

        while True:
            places = merge(text, places)
            if places == merge(text, places):
                return places

    def find_potential_places(self):
        text = self.tweet.content
        if text == '':
            return []

        text  = self.separate_words_divided_by_slash(text)
        text  = self.remove_hashtags_and_at_sign(text)
        words = self.find_words_with_capital_letter(text)
        words = self.remove_words_with_numbers(words)
        words = self.remove_words_with_only_capital_letters(words)
        words = self.remove_short_words(words)
        words = self.remove_trailing_symbols(words)
        words = self.remove_stopwords(words)
        words = self.merge_words_that_are_next_to_each_other(words)
        words = self.remove_duplicate_words(words)
        words = sorted(words)
        return words
