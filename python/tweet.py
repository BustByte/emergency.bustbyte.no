class Tweet:

    def __init__(self):
        self.id = None
        self.content = None
        self.timestamp = None
        self.user = None

    def __repr__(self):
        return '<Tweet:user=%s, content=%s, id=%s, timestamp=%s>' % (
            self.user, self.content, self.id, self.timestamp
        )
