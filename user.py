class User:
    def __init__(self, username=None):
        self.username = username

    def __repr__(self):
        return self.username
