import json

class Query:

    def __init__(self, event=None, evidence=None):
        self._event = event
        self._evidence = evidence
        self.end_date = None
        self.start_date = None

    @property
    def event(self):
        return self._event[0].upper() + self._event[1:] \
            if self._event else None

    @property
    def evidence(self):
        return self._evidence[0].upper() + self._evidence[1:] \
            if self._evidence else None

    @event.setter
    def event(self, event):
        self._event = event

    @evidence.setter
    def evidence(self, evidence):
        self._evidence = evidence

    @staticmethod
    def from_json(json_string):
        parsed = json.loads(json_string)
        query = Query(event=None, evidence=None)

        query._event = parsed['event'] \
            if parsed['event'] else None

        query._evidence = parsed['evidence'] \
            if parsed['evidence'] else None

        query.start_date = parsed['startDate']
        query.end_date = parsed['endDate']
        return query
