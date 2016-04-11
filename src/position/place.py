class Place:

    def __init__(self, name=None, id=None):
        self.id = id
        self.name = name

    def __repr__(self):
        return '<Place:id=%s, name=%s>' % (
            self.id, self.name
        )
