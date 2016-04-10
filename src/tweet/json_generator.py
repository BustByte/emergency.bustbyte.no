from tweet.tweet import Tweet
from position.position import Position
import random

class Json:

    @classmethod
    def generate_json(cls, tweets):
        json_tweets = []
        for tweet in tweets:
            lat = random.uniform(58.1, 70.1)
            lng = random.uniform(4.6, 30.1)
            json_tweet = {
                'position': {
                    'lat': lat,
                    'lng': lng
                },
                'id': tweet.id
            }
            json_tweets.append(json_tweet)
        return json_tweets
