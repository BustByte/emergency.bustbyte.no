import json
import requests 
from config import configuration
from ontology import Query

class Tunnel:

    port = configuration['ontology']['port']
    host = configuration['ontology']['tunnel']
    page = configuration['ontology']['page']

    def push(self, tweet):
        # This is where are supposed to send new tweets
        pass

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
