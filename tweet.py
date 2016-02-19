class Tweet:

    def __init__(self):
        self.id = None
        self.content = None
        self.timestamp = None

    def __repr__(self):
        return '<Tweet:id=%s, timestamp=%s, content=%s>' % (
            self.id, self.timestamp, self.content
        )
