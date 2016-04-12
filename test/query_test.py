from unittest import TestCase
from unittest.mock import MagicMock
from ontology import Query

class TestQuery(TestCase):

    def test_it_can_be_construct_evidence_from_a_json_string(self):
        json = '''{ "evidence": "knife", "event": "robbery", "startDate": "2014-01-01", "endDate": "2015-01-01"  }'''
        query = Query.from_json(json)
        self.assertEqual(query.evidence, 'Knife')
    
    def test_it_can_be_construct_event_from_a_json_string(self):
        json = '''{ "evidence": "knife", "event": "robbery", "startDate": "2014-01-01", "endDate": "2015-01-01"  }'''
        query = Query.from_json(json)
        self.assertEqual(query.event, 'Robbery')

    def test_it_does_not_mess_up_internal_capitalization_only_first_letter(self):
        json = '''{ "evidence": "knife", "event": "trafficCollision", "startDate": "2014-01-01", "endDate": "2015-01-01"  }'''
        query = Query.from_json(json)
        self.assertEqual(query.event, 'TrafficCollision')

    def test_it_ignores_event_if_it_is_not_provided(self):
        json = '''{ "evidence": "knife", "event": false, "startDate": "2014-01-01", "endDate": "2015-01-01"  }'''
        query = Query.from_json(json)
        self.assertEqual(query.event, None)

    def test_it_ignores_evidence_if_it_is_not_provided(self):
        json = '''{ "evidence": false, "event": false, "startDate": "2014-01-01", "endDate": "2015-01-01"  }'''
        query = Query.from_json(json)
        self.assertEqual(query.evidence, None)

    def test_it_can_be_construct_start_date_from_a_json_string(self):
        json = '''{ "evidence": "knife", "event": "robbery", "startDate": "2014-01-01", "endDate": "2015-01-01"  }'''
        query = Query.from_json(json)
        self.assertEqual(query.start_date, '2014-01-01')

    def test_it_can_be_construct_end_date_from_a_json_string(self):
        json = '''{ "evidence": "knife", "event": "robbery", "startDate": "2014-01-01", "endDate": "2015-01-01"  }'''
        query = Query.from_json(json)
        self.assertEqual(query.end_date, '2015-01-01')
