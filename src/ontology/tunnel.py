import json
import requests
from config import configuration
from ontology import Query
from tweet.json_generator import Json

class Tunnel:

    port = configuration['ontology']['port']
    host = configuration['ontology']['tunnel']
    page = configuration['ontology']['page']
    add_tweets = configuration['ontology']['add_tweets']

    def push(self, tweets):
        url = '{0}:{1}/{2}'.format(self.host, self.port, self.add_tweets)
        json = Json.generate_ontology_json(tweets)
        requests.post(url, data=json)

    def get_result_ids(self, query):
        url = '{0}:{1}/{2}'.format(self.host, self.port, self.page)
        response = requests.get(url, params={
            'event': query.event,
            'evidence': query.evidence
        })
        return json.loads(response.text)

    def pull(self, query):
        result_ids = self.get_result_ids(query)
        return result_ids
