from unittest import TestCase
from unittest.mock import MagicMock
from locator import ScoreCalculator

class TestScorer(TestCase):

    def setUp(self):
        self.tweet = MagicMock(content=None)

    def test_is_given_score_negative_1_if_word_not_in_tweet(self):
        self.tweet.content = 'Ås: UP har vært på kontroll'
        score = ScoreCalculator(self.tweet).for_word('Drøbak')
        self.assertEqual(score, -1)

    def test_first_word_in_tweet_followed_by_colon_is_given_a_greater_score_than_one_at_the_end(self):
        self.tweet.content = 'Ås: UP har vært på kontroll ved Universitet.'
        aas_score = ScoreCalculator(self.tweet).for_word('Ås')
        university_score = ScoreCalculator(self.tweet).for_word('Universitet')
        self.assertGreater(aas_score, university_score)

    def test_word_in_tweet_followed_by_colon_is_given_a_greater_score_than_one_at_the_end(self):
        self.tweet.content = 'Hordaland, Voss: UP har vært på kontroll ved Bioform.'
        voss_score = ScoreCalculator(self.tweet).for_word('Voss')
        bioform_score = ScoreCalculator(self.tweet).for_word('Bioform')
        self.assertGreater(voss_score, bioform_score)

    def test_word_following_a_comma_has_a_greater_score_than_one_that_is_not(self):
        self.tweet.content = 'Trondheim, Tiller har Brann supporterne gjort opprør.'
        brann_score = ScoreCalculator(self.tweet).for_word('Brann')
        tiller_score = ScoreCalculator(self.tweet).for_word('Tiller')
        self.assertLess(brann_score, tiller_score)

    def test_word_followed_by_a_comma_has_same_score_as_one_that_is_followed_by_a_comma(self):
        self.tweet.content = 'Live: Trondheim, Tiller, har supporterne til Brann gjort opprør.'
        tiller_score = ScoreCalculator(self.tweet).for_word('Tiller')
        trondheim_score = ScoreCalculator(self.tweet).for_word('Trondheim')
        self.assertEqual(tiller_score, trondheim_score)

    def test_a_word_in_start_of_sentence_has_lower_score_than_one_that_is_not(self):
        self.tweet.content = 'Brann og Redningsetaten er på vei. Oslo er folksomt nå.'
        oslo_score = ScoreCalculator(self.tweet).for_word('Oslo')
        redningsetaten_score = ScoreCalculator(self.tweet).for_word('Redningsetaten')
        self.assertLess(oslo_score, redningsetaten_score)

    def test_a_word_in_middle_of_sentence_has_higher_score_than_one_that_is_at_the_start_of_the_sentence(self):
        self.tweet.content = 'Trondheim har mye regn og det har Tiller også.'
        tiller_score = ScoreCalculator(self.tweet).for_word('Tiller')
        trondheim_score = ScoreCalculator(self.tweet).for_word('Trondheim')
        self.assertLess(trondheim_score, tiller_score)

    def test_a_word_followed_by_a_preposition_is_given_a_higher_score_than_one_that_is_not(self):
        self.tweet.content = 'Tyveri i Trondheim. Kanskje også Tiller.'
        tiller_score = ScoreCalculator(self.tweet).for_word('Tiller')
        trondheim_score = ScoreCalculator(self.tweet).for_word('Trondheim')
        self.assertGreater(trondheim_score, tiller_score)

    def test_a_word_followed_by_a_uppercased_preposition_is_given_a_higher_score_than_one_that_is_not(self):
        self.tweet.content = 'I Trondheim. Kanskje også Tiller.'
        tiller_score = ScoreCalculator(self.tweet).for_word('Tiller')
        trondheim_score = ScoreCalculator(self.tweet).for_word('Trondheim')
        self.assertGreater(trondheim_score, tiller_score)
