from tweet import Tweet
from datetime import datetime

class Mapper:

    @classmethod
    def to_row(cls, tweet):
        row = {}

        row['id'] = tweet.id

        row['user'] = tweet.user.username \
            if tweet.user else None

        row['name'] = tweet.user.name \
            if tweet.user else None

        row['content'] = tweet.content

        row['timestamp'] = tweet.timestamp

        return row 

    @classmethod
    def to_tweet(cls, row):
        tweet = Tweet()

        if 'id' in row.keys():
            tweet.id = row['id']

        if 'content' in row.keys():
            tweet.content = row['content']

        if 'timestamp' in row.keys():
            tweet.timestamp = cls.convert_timestamp(row['timestamp'])

        return tweet

    @classmethod
    def convert_timestamp(cls, timestamp):
        try:
            return datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            return None
