class Place:

    def __init__(self, name=None, id=None, commune_name=None):
        self.name = name
        self.id = id
        self.commune_name = commune_name

    def __repr__(self):
        return '<Place:id=%s, name=%s, commune_name=%s>' % (
            self.id, self.name, self.commune_name
        )
