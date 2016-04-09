import os
from datetime import datetime, timedelta
from twitter import *
from tweet import Tweet
from user import User
from twitter_listener import OAuthSettings
from database import Database

users = """politihedmark
Opssunnmore
opsenfollo
politietostfold
politiopssbusk
OPSostfinnmark
PolitiOstfldOPS
HedmarkOPS
politiNTrondops
polititroms
RomerikePoliti
polititelemark
ABpolitiops
politietoslo""".split('\n')

class TwitterDownloader:

    def __init__(self):
        self.authSettings = OAuthSettings()
        self.twitter_download = Twitter(auth=self.authSettings.get_oauth_settings())

    def get_tweets(self, username, max_id=None):
        if max_id:
            tweets = self.twitter_download.statuses.user_timeline(max_id=max_id, count=200, screen_name=username)
        else:
            tweets = self.twitter_download.statuses.user_timeline(count=200, screen_name=username)

        return [tweet for tweet in tweets if not tweet['retweeted']]

    def convert(self, twitter_object):
        try:
            tweet = Tweet()
            tweet.user = User(twitter_object['user']['name'], twitter_object['user']['screen_name'])
            tweet.id = twitter_object['id_str']
            tweet.content = twitter_object['text']
            tweet.timestamp = self.convert_to_sane_date(twitter_object['created_at'])
        except KeyError:
            pass 
        return tweet

    def convert_to_sane_date(self, insane_date):
        insane_date = insane_date[4:]
        sane_date = datetime.strptime(insane_date, '%b %d %H:%M:%S +0000 %Y')
        added_hour = sane_date + timedelta(hours=1)
        return added_hour

    def save_to_db(self, external_tweets):
        print("Saved %d tweets to the db" % len(external_tweets))
        internal_tweets = [self.convert(external_tweet) for external_tweet in external_tweets]
        Database.save_all(internal_tweets)
        return len(external_tweets)

    def listen_to_twitter(self, username):
        tweets = self.get_tweets(username)
        self.save_to_db(tweets)
        latest_id = None

        while True:
            tweets = self.get_tweets(username, latest_id) 
            latest_id = tweets[len(tweets)-1]['id_str']
            number_saved = self.save_to_db(tweets)
            if number_saved < 3:
                break 

Database.setup()
downloader = TwitterDownloader()

for user in users:
    print('Downloading for %s' % user)
    downloader.listen_to_twitter(user)
