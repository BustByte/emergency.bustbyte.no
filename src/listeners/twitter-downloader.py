import os
import sys
from twisted.python import log
from datetime import datetime, timedelta
from twitter import *
from tweet.tweet import Tweet
from user import User
from listeners.twitter_listener import OAuthSettings
from listeners import TimeConverter
from database.database import Database
from processor.processor import Processor

users = """ABpolitiops
AgderOPS
HaugSunnOps
HedmarkOPS
HelgelandOPS
Hordalandpoliti
opsenfollo
OPSGudbrandsdal
opsnbuskerud
OPSostfinnmark
Opssunnmore
oslopolitiops
politietoslo
politietostfold
politietsognfj
politihedmark
politiMHPD
PolitiNoRoOps
politiNTrondops
politiopssbusk
politiOpsSTPD
PolitiOstfldOPS
polititelemark
polititroms
PolitiVestfinnm
PolitiVestfold
PolitiVestoppla
Rogalandops
RomerikePoliti
Saltenpolitiet""".split('\n')

last_tweet_id_in_db = 704318205976813572

class TwitterDownloader:

    def __init__(self):
        print("Booting tweet processor...")
        self.processor = Processor()
        print("Tweet processor successfully booted")
        self.authSettings = OAuthSettings()
        self.twitter_download = Twitter(auth=self.authSettings.get_oauth_settings())

    def get_tweets(self, username, since_id=None, max_id=None):
        if max_id:
            tweets = self.twitter_download.statuses.user_timeline(since_id=since_id, max_id=max_id, count=200, screen_name=username)
        else:
            tweets = self.twitter_download.statuses.user_timeline(since_id=since_id, count=200, screen_name=username)

        return [self.convert(tweet) for tweet in tweets if not 'retweeted_status' in tweet]

    def convert(self, twitter_object):
        try:
            tweet = Tweet()
            tweet.user = User(twitter_object['user']['name'], twitter_object['user']['screen_name'])
            tweet.id = twitter_object['id_str']
            tweet.content = twitter_object['text']
            tweet.timestamp = TimeConverter.twitter_time_to_date_string(twitter_object['created_at'])
        except KeyError:
            pass
        return tweet

    def download_user_tweets(self, username):
        latest_id = None
        total_for_user = 0
        while True:
            if latest_id:
                tweets = self.get_tweets(username=username, since_id=last_tweet_id_in_db, max_id=latest_id)
            else:
                tweets = self.get_tweets(username=username, since_id=last_tweet_id_in_db)

            total_for_user += len(tweets)
            print("Received %s new tweets, in total %s for %s." % (len(tweets), total_for_user, username))

            if (len(tweets)):
                latest_id = int(tweets[len(tweets)-1].id)
                self.processor.process_many(tweets)

            if (len(tweets) < 200):
                break
        return total_for_user

if __name__ == '__main__':
    log.startLogging(sys.stdout)
    downloader = TwitterDownloader()
    total_for_all = 0

    for index, username in enumerate(users):
        print('[%s av %s] - Downloading tweets for %s' % (index+1, len(users), username))
        total_for_all += downloader.download_user_tweets(username)

    print("Download complete, %s tweets were downloaded in total." % (total_for_all))
