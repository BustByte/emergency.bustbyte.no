class User:
    def __init__(self, name=None, username=None):
        self.name = name
        self.username = username

    def __repr__(self):
        return self.name
