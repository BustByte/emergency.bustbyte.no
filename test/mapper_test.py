from unittest import TestCase
from unittest.mock import MagicMock
from datetime import datetime
from database import Mapper

class TestMapper(TestCase):

    def setUp(self):
        self.user = MagicMock(
            username=None,
            name=None
        )
        self.tweet = MagicMock(
            id=None,
            content=None,
            user=self.user
        )

    def test_it_maps_id_to_row(self):
        self.tweet.id = '303034'
        row = Mapper.to_row(self.tweet)
        self.assertEqual(row['id'], '303034')

    def test_it_maps_id_to_tweet(self):
        row = {'id': '303034'}
        tweet = Mapper.to_tweet(row)
        self.assertEqual(tweet.id, '303034')

    def test_it_maps_content_to_row(self):
        self.tweet.content = 'Mye kriminalitet i sentrum.'
        row = Mapper.to_row(self.tweet)
        self.assertEqual(row['content'], 'Mye kriminalitet i sentrum.')

    def test_it_maps_content_to_tweet(self):
        row = {'content': 'Mye kriminalitet i sentrum.'}
        tweet = Mapper.to_tweet(row)
        self.assertEqual(tweet.content, 'Mye kriminalitet i sentrum.')

    def test_it_maps_username_to_row(self):
        self.tweet.user.username = 'oslopoliti'
        row = Mapper.to_row(self.tweet)
        self.assertEqual(row['user'], 'oslopoliti')
    
    def test_it_maps_timestamp_to_tweet(self):
        row = {'timestamp': '2013-08-13 11:00:13'}
        tweet = Mapper.to_tweet(row)
        self.assertEqual(tweet.timestamp, datetime(2013, 8, 13, 11, 0, 13))

    def test_it_can_map_a_tweet_with_messed_up_timestamp(self):
        row = {'timestamp': 'Tzo4OiJzdGRDbGFzcyI6Mzp7czo0OiJ1cmxzIjthOjA6e31zOjEzOiJ1c2VyX21lbnRpb25zIjthOjA6e31zOjg6Imhhc2h0YWdzIjthOjA6e319'}
        tweet = Mapper.to_tweet(row)
        self.assertEqual(tweet.timestamp, None)
