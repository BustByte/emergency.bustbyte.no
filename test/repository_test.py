from unittest import TestCase
from unittest.mock import MagicMock
from database import Database, Repository
from user import User
from tweet import Tweet
from ontology import Query
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
        self.tweet.content = 'Hva skjer?'
        self.tweet.timestamp = '2014-01-01 10:10:10'
        self.tweet.position = self.position

        self.search_query = {
            'query': None,
            'startDate': None,
            'endDate': None
        }

        self.category_query = Query.from_json('''{
            "evidence": "weapon",
            "event": "fire",
            "startDate": "2013-12-12",
            "endDate": "2017-03-31"
        }''')

    def tearDown(self):
        Database.tear_down()

    def test_it_also_saves_the_user_account(self):
        Repository.create(self.tweet)
        stored_tweet = Repository.read('1234')
        assert stored_tweet.user.username == 'opsenoslo'

    def test_it_get_all_the_tweets(self):
        stored_tweets = Repository.all()
        assert len(stored_tweets) == 2

    def test_it_can_return_all_the_places_by_username(self):
        Repository.create(self.tweet)
        communes, places = Repository.all_users_with_places()
        self.assertIn('opsenoslo', places)
        self.assertEqual(places['opsenoslo']['Vestby'].commune_name, 'Oslo')

    def test_it_can_return_all_the_places_by_commune(self):
        Repository.create(self.tweet)
        communes, places = Repository.all_users_with_places()
        #self.assertIn('Oslo', communes)
        self.assertEqual(communes['opsenoslo']['Oslo']['Vestby'].commune_name, 'Oslo')

    def test_it_matches_place_if_it_has_a_symbol_behind_it(self):
        Repository.create(self.tweet)
        self.search_query['query'] = 'Oslo'
        self.search_query['startDate'] = '2013-12-31'
        self.search_query['endDate'] = '2014-05-05'
        results = Repository.search(self.search_query)
        self.assertEqual(len(results), 1)

    def test_it_does_not_matche_tweet_if_it_is_published_outside_the_interval(self):
        self.tweet.content = 'Snakkes i Ås hadebra.'
        Repository.create(self.tweet)
        self.search_query['query'] = 'Vestby'
        self.search_query['startDate'] = '2010-01-31'
        self.search_query['endDate'] = '2010-05-05'
        results = Repository.search(self.search_query)
        self.assertEqual(len(results), 0)

    def test_it_matches_place_wrapped_in_parenthesis(self):
        self.tweet.content = 'Snakkes i (Oslo) hadebra.'
        Repository.create(self.tweet)
        self.search_query['query'] = 'Oslo'
        self.search_query['startDate'] = '2013-12-31'
        self.search_query['endDate'] = '2014-05-05'
        results = Repository.search(self.search_query)
        self.assertEqual(len(results), 1)

    def test_it_matches_superstring(self):
        self.tweet.content = 'Snakkes i Åsane hadebra.'
        Repository.create(self.tweet)
        self.search_query['query'] = 'Ås'
        self.search_query['startDate'] = '2013-12-31'
        self.search_query['endDate'] = '2014-05-05'
        results = Repository.search(self.search_query)
        self.assertEqual(len(results), 1)

    def test_it_matches_place_followed_by_exclamation_point(self):
        self.tweet.content = 'Snakkes i Ås! hadebra.'
        Repository.create(self.tweet)
        self.search_query['query'] = 'Ås'
        self.search_query['startDate'] = '2013-12-31'
        self.search_query['endDate'] = '2014-05-05'
        results = Repository.search(self.search_query)
        self.assertEqual(len(results), 1)

    def test_it_matches_place_followed_by_question_mark(self):
        self.tweet.content = 'Snakkes i Ås? hadebra.'
        Repository.create(self.tweet)
        self.search_query['query'] = 'Ås'
        self.search_query['startDate'] = '2013-12-31'
        self.search_query['endDate'] = '2014-05-05'
        results = Repository.search(self.search_query)
        self.assertEqual(len(results), 1)

    def test_it_matches_place_wrapped_by_dots(self):
        self.tweet.content = 'Snakkes i .Ås. hadebra.'
        Repository.create(self.tweet)
        self.search_query['query'] = 'Ås'
        self.search_query['startDate'] = '2013-12-31'
        self.search_query['endDate'] = '2014-05-05'
        results = Repository.search(self.search_query)
        self.assertEqual(len(results), 1)

    def test_it_matches_place_wrapped_by_commas(self):
        self.tweet.content = 'Snakkes i ,Ås, hadebra.'
        Repository.create(self.tweet)
        self.search_query['query'] = 'Ås'
        self.search_query['startDate'] = '2013-12-31'
        self.search_query['endDate'] = '2014-05-05'
        results = Repository.search(self.search_query)
        self.assertEqual(len(results), 1)

    def test_it_matches_place_wrapped_by_spaces(self):
        self.tweet.content = 'Snakkes i Ås hadebra.'
        Repository.create(self.tweet)
        self.search_query['query'] = 'Ås'
        self.search_query['startDate'] = '2013-12-31'
        self.search_query['endDate'] = '2014-05-05'
        results = Repository.search(self.search_query)
        self.assertEqual(len(results), 1)

    def test_it_matches_at_sign_followed_by_place(self):
        self.tweet.content = 'Snakkes i @Ås hadebra.'
        Repository.create(self.tweet)
        self.search_query['query'] = 'Ås'
        self.search_query['startDate'] = '2013-12-31'
        self.search_query['endDate'] = '2014-05-05'
        results = Repository.search(self.search_query)
        self.assertEqual(len(results), 1)

    def test_it_matches_hashtag_followed_by_place(self):
        self.tweet.content = 'Snakkes i #Ås hadebra.'
        Repository.create(self.tweet)
        self.search_query['query'] = 'Ås'
        self.search_query['startDate'] = '2013-12-31'
        self.search_query['endDate'] = '2014-05-05'
        results = Repository.search(self.search_query)
        self.assertEqual(len(results), 1)

    def test_it_matches_place_followed_by_colon(self):
        self.tweet.content = 'Snakkes i Ås: hadebra.'
        Repository.create(self.tweet)
        self.search_query['query'] = 'Ås'
        self.search_query['startDate'] = '2013-12-31'
        self.search_query['endDate'] = '2014-05-05'
        results = Repository.search(self.search_query)
        self.assertEqual(len(results), 1)

    def test_it_matches_place_followed_by_semi_colon(self):
        self.tweet.content = 'Snakkes i Ås; hadebra.'
        Repository.create(self.tweet)
        self.search_query['query'] = 'Ås'
        self.search_query['startDate'] = '2013-12-31'
        self.search_query['endDate'] = '2014-05-05'
        results = Repository.search(self.search_query)
        self.assertEqual(len(results), 1)

    def test_it_matches_place_followed_by_slash(self):
        self.tweet.content = 'Snakkes i Ås/Vestby hadebra.'
        Repository.create(self.tweet)
        self.search_query['query'] = 'Ås'
        self.search_query['startDate'] = '2013-12-31'
        self.search_query['endDate'] = '2014-05-05'
        results = Repository.search(self.search_query)
        self.assertEqual(len(results), 1)

    def test_it_matches_slash_followed_by_place(self):
        self.tweet.content = 'Snakkes i Ås/Vestby hadebra.'
        Repository.create(self.tweet)
        self.search_query['query'] = 'Vestby'
        self.search_query['startDate'] = '2013-12-31'
        self.search_query['endDate'] = '2014-05-05'
        results = Repository.search(self.search_query)
        self.assertEqual(len(results), 1)

    def test_it_matches_place_followed_by_quote(self):
        self.tweet.content = "Snakkes i Vestby's gater hadebra."
        Repository.create(self.tweet)
        self.search_query['query'] = 'Vestby'
        self.search_query['startDate'] = '2013-12-31'
        self.search_query['endDate'] = '2014-05-05'
        results = Repository.search(self.search_query)
        self.assertEqual(len(results), 1)

    def test_it_can_read_multiple_tweets(self):
        Repository.create(self.tweet)
        self.tweet.id = '4321'
        Repository.create(self.tweet)
        self.tweet.id = '54321'
        Repository.create(self.tweet)
        results = Repository.read_multiple(['1234', '4321'], self.category_query)
        self.assertEqual(len(results), 2)

    def test_it_can_read_multiple_tweets_between_dates(self):
        results = Repository.read_multiple(['1234', '4321'], self.category_query)
        self.assertEqual(len(results), 2)

    def test_it_can_read_positions(self):
        position = Repository.get_position(1)
        assert position.latitude == '59.3434'
        assert position.longitude == '18.3434'
