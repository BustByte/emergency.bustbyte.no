from unittest import TestCase
from unittest.mock import MagicMock
from processor import Processor
from database import Database
from database import Repository
from user import User
from tweet import Tweet
from position import Position

class TestProcessor(TestCase):



    def setUp(self):
        Database.setup()

        self.user = User()
        self.user.name = 'Oslo Operasjonssentral'
        self.user.username = 'opsenoslo'

        self.tweet = Tweet()
        self.tweet.id = '4321'
        self.tweet.user = self.user
        self.tweet.content = 'Vestby, Oslo: En hund har blitt påkjørt.'
        self.tweet.timestamp = '2014-01-01 10:10:10'

    def tearDown(self):
        Database.tear_down()

    def test_processor_creates_a_tweet_in_the_database(self):
        processor = Processor()
        processor.process(self.tweet)
        stored_tweet = Repository.read('4321')
        assert stored_tweet.id == '4321'

    def test_processor_adds_a_position_to_the_tweet(self):
        processor = Processor()
        stored_tweet = processor.process(self.tweet)
        assert stored_tweet.position.latitude != None
        assert stored_tweet.position.longitude != None

    def test_processor_stores_tweet_even_if_no_place_matched(self):
        self.tweet.content = 'Westby, Åslo: En hund har blitt påkjørt.'
        processor = Processor()
        stored_tweet = processor.process(self.tweet)  
        assert stored_tweet.position.latitude == None
        assert stored_tweet.position.longitude == None
