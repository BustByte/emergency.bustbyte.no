from unittest import TestCase
from unittest.mock import MagicMock, patch
from ontology import Tunnel
from ontology import Query

class TestTunnel(TestCase):

    @patch('ontology.tunnel.requests')
    def test_pull_returns_a_list_of_tweet_ids(self, requests):
        requests.get.return_value = MagicMock(text='["1234", "4321"]')
        tunnel = Tunnel()
        query = Query(event='injuri', evidence='knife')
        ids = tunnel.get_result_ids(query)
        self.assertEqual(ids, ['1234', '4321'])

    @patch('ontology.tunnel.requests')
    def test_pull_returns_an_empty_list_of_tweet_ids_if_empty_result(self, requests):
        requests.get.return_value = MagicMock(text='[]')
        tunnel = Tunnel()
        query = Query(event='injuri', evidence='knife')
        ids = tunnel.get_result_ids(query)
        self.assertEqual(ids, [])
