from unittest import TestCase
from unittest.mock import MagicMock
from tweet import Tweet
from database import Database, Repository 

class TestRepository(TestCase):

    def test_it_save_a_tweet(self):
        Database.setup()
        tweet = Tweet()
        tweet.id = '1234'
        Repository.create(tweet)
        stored_tweet = Repository.read('1234')
        assert stored_tweet is not None

