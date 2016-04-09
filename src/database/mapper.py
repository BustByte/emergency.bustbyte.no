from tweet import Tweet
from datetime import datetime

class Mapper:

    @classmethod
    def to_row(cls, tweet):
        row = {}
        row['id'] = tweet.id
        row['user'] = tweet.user.username
        row['name'] = tweet.user.name
        row['content'] = tweet.content
        row['timestamp'] = tweet.timestamp
        return row 

    @classmethod
    def to_tweet(cls, row):
        tweet = Tweet()

        tweet.id = row['id'] \
            if 'id' in row else None

        tweet.content = row['content'] \
            if 'content' in row else None

        tweet.timestamp = datetime.strptime(row['timestamp'], '%Y-%m-%d %H:%M:%S')  \
            if 'timestamp' in row else None

        return tweet
