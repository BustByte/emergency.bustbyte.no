from database import Database
from fetcher import Fetcher
from extractor import Extractor
from user import User

class Scraper:

    base_url = 'https://mobile.twitter.com'

    def get_profile_url(self, user):
        return self.base_url + '/' + user.username

    def get_tweet_url(self, user, tweet_id):
        return self.get_profile_url(user) + '/status/' + tweet_id

    def get_twitter_ids(self, user, since):
        url = self.get_profile_url(user) + '?max_id=' + since
        html = Fetcher.request(url)
        print('Successfully retrieved new ids.')
        return Extractor.extract_tweet_ids(html)

    def get_single_tweet(self, user, tweet_id):
        tweet_url = self.get_tweet_url(user, tweet_id)
        html = Fetcher.request(tweet_url)
        tweet = Extractor.extract_tweet(html)
        print('Successfully retrieved %s' % tweet_id)
        return tweet

    def get_tweets_since(self, user, since):
        tweets = []
        for tweet_id in self.get_twitter_ids(user, since):
            tweet = self.get_single_tweet(user, tweet_id)
            tweet.user = user
            tweets.append(tweet)
        return tweets

if __name__ == '__main__':
    Database.setup()

    scraper = Scraper()
    user = User('oslopolitiops')
    since_id = '700125837232885760'

    tweets = scraper.get_tweets_since(user, since_id)
    Database.save_all(tweets)

    while True:
        latest_id = tweets[len(tweets) - 1].id
        tweets = scraper.get_tweets_since(user, latest_id)
        Database.save_all(tweets)
