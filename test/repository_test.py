from unittest import TestCase
from unittest.mock import MagicMock
from tweet import Tweet
from database import Database, Repository 

class TestRepository(TestCase):

    def setUp(self):
        Database.setup()

        self.tweet = Tweet()
        self.tweet.id = '1234'
        self.tweet.content = 'Hello world'
        self.tweet.user = MagicMock(username='lol')
        self.tweet.user.name = 'rofl'
        self.tweet.timestamp = '2014-01-01 10:10:10'


    def tearDown(self):
        Database.tear_down()

    def test_it_can_save_a_tweet(self):
        Repository.create(self.tweet)
        stored_tweet = Repository.read('1234')
        assert stored_tweet.id == '1234'
        assert stored_tweet.content == 'Hello world'
        #assert stored_tweet.user.name == 'rofl'
