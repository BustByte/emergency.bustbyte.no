from unittest import TestCase
from unittest.mock import MagicMock
from database import Database, Repository 
from user import User
from tweet import Tweet
from position import Position

class TestRepository(TestCase):

    def setUp(self):
        Database.setup()

        self.user = User()
        self.user.name = 'Oslo Operasjonssentral'
        self.user.username = 'opsenoslo'

        self.position = Position()
        self.position.latitude = '59.47437473'
        self.position.longitude = '10.4557473'

        self.tweet = Tweet()
        self.tweet.id = '1234'
        self.tweet.user = self.user
        self.tweet.content = 'Hello world'
        self.tweet.timestamp = '2014-01-01 10:10:10'
        self.tweet.position = self.position

    def tearDown(self):
        Database.tear_down()

    def test_it_can_save_a_tweet(self):
        Repository.create(self.tweet)
        stored_tweet = Repository.read('1234')
        assert stored_tweet.id == '1234'
        assert stored_tweet.content == 'Hello world'

    def test_it_also_saves_the_user_account(self):
        Repository.create(self.tweet)
        stored_tweet = Repository.read('1234')
        assert stored_tweet.user.name == 'Oslo Operasjonssentral'
        assert stored_tweet.user.username == 'opsenoslo'

    def test_it_get_all_the_tweets(self):
        Repository.create(self.tweet)
        Repository.create(self.tweet)
        stored_tweets = Repository.all()
        assert len(stored_tweets) == 2
