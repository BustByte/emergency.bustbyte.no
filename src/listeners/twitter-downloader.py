import os
from datetime import datetime, timedelta
from twitter import *
from tweet.tweet import Tweet
from user.user import User
from twitter_listener import OAuthSettings
from database import Database
from processor import Processor

users = """OPSostfinnmark
PolitiVestfinnm
polititroms
politiMHPD
politiMHPD
Saltenpolitiet
HelgelandOPS
politiOpsSTPD
politiNTrondops
Opssunnmore
412278318
PolitiNoRoOps
Hordalandpoliti
politietsognfj
Rogalandops
HaugSunnOps
AgderOPS
opsnbuskerud
politiopssbusk
PolitiVestfold
polititelemark
oslopolitiops
politietoslo
ABpolitiops
opsenfollo
RomerikePoliti
PolitiOstfldOPS
politietostfold
OPSGudbrandsdal
politihedmark
HedmarkOPS
PolitiVestoppla
""".split('\n')

lastest_tweet_id = float(704318205976813572)

class TwitterDownloader:

    def __init__(self):
        self.authSettings = OAuthSettings()
        self.twitter_download = Twitter(auth=self.authSettings.get_oauth_settings())

    def get_tweets(self, username, max_id=None):
        if max_id:
            tweets = self.twitter_download.statuses.user_timeline(max_id=max_id, count=200, screen_name=username)
        else:
            tweets = self.twitter_download.statuses.user_timeline(count=200, screen_name=username)

        return [convert(tweet) for tweet in tweets if not tweet['retweeted']]

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
        Processor.process_many(tweets)
        latest_id = lastest_tweet_id + 1

        while latest_id > lastest_tweet_id:
            tweets = self.get_tweets(username, latest_id)
            latest_id = float(tweets[len(tweets)-1]['id_str'])
            Processor.process_many(tweets)

downloader = TwitterDownloader()

for user in users:
    print('Downloading for %s' % user)
    downloader.listen_to_twitter(user)
