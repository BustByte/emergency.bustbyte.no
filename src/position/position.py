class Position:

    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude

    def __repr__(self):
        return '(%s, %s)' % (self.latitude, self.longitude)
