class Tweet:

    def __init__(self):
        self.id = None
        self.user = None
        self.content = None
        self.position = None
        self.timestamp = None

    def __repr__(self):
        return '<Tweet:id=%s, timestamp=%s, position=%s, user=%s, content="%s" position=%s>' % (
            self.id, self.timestamp, self.position, self.user, self.content, self.position
        )
