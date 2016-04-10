class ScoreCalculator:

    def __init__(self, tweet):
        self.tweet = tweet

    def is_at_start_of_tweet(self, word):
        return self.tweet.content.startswith(word)

    def is_the_first_word_followed_by_colon(self, word):
        return self.is_at_start_of_tweet(word) and \
            self.tweet.content.startswith(word + ':')

    def is_word_followed_by_colon(self, word):
        return self.is_word_in_tweet(word + ':')

    def is_word_in_tweet(self, word):
        return word in self.tweet.content

    def is_next_to_a_comma(self, word):
        return ', ' + word in self.tweet.content or \
            word + ', ' in self.tweet.content

    def is_at_start_of_sentence(self, word):
        return '. ' + word in self.tweet.content

    def is_following_a_preposition(self, word):
        prepositions = [
            'ved', 'på', 'i',
            'rundt', 'av', 'mellom',
            'rundt', 'omkring', 'mot',
            'over', 'under', 'fra', 'til'
        ]
        return any(preposition + ' ' + word.lower() in self.tweet.content.lower() \
            for preposition in prepositions)

    def for_word(self, word):
        if not self.is_word_in_tweet(word):
            return -1

        score  = 0
        score += 10 if self.is_next_to_a_comma(word) else 0
        score += 10 if self.is_at_start_of_tweet(word) else 0
        score += 10 if not self.is_at_start_of_sentence(word) else 0
        score += 25 if self.is_the_first_word_followed_by_colon(word) else 0
        score += 15 if self.is_following_a_preposition(word) else 0
        score += 20 if self.is_word_followed_by_colon(word) else 0

        return score
