from user import User
from tweet import Tweet
from position import Place
from position import Position
from datetime import datetime

class Mapper:

    @classmethod
    def to_row(cls, tweet):
        row = {}

        row['id'] = str(tweet.id)

        row['username'] = tweet.user.username \
            if tweet.user else None

        row['name'] = tweet.user.name \
            if tweet.user else None

        row['content'] = tweet.content

        row['timestamp'] = tweet.timestamp

        return row

    @classmethod
    def to_tweet(cls, row):
        tweet = Tweet()
        tweet.user = User()
        tweet.position = Position()

        if 'id' in row.keys():
            tweet.id = row['id']

        if 'content' in row.keys():
            tweet.content = row['content']

        if 'timestamp' in row.keys():
            tweet.timestamp = cls.convert_timestamp(row['timestamp'])

        if 'username' in row.keys():
            tweet.user.username = row['username']

        if 'name' in row.keys():
            tweet.user.name = row['name']

        if 'latitude' in row.keys():
            tweet.position.latitude = row['latitude']

        if 'longitude' in row.keys():
            tweet.position.longitude = row['longitude']

        return tweet

    @classmethod
    def to_place(cls, row):
        place = Place()

        if 'id' in row.keys():
            place.id = row['id']

        if 'place_name' in row.keys():
            place.name = row['place_name']

        if 'commune_name' in row.keys():
            place.commune_name = row['commune_name']

        return place

    @classmethod
    def convert_timestamp(cls, timestamp):
        try:
            return datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            return None
