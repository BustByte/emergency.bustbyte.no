from datetime import datetime
from bs4 import BeautifulSoup
from tweet import Tweet

class Extractor:

    @classmethod
    def extract_tweet_ids(cls, html):
        soup = BeautifulSoup(html, 'html.parser')
        tweet_tables = soup.select('table.tweet')
        return [cls.extract_id(tweet_table) \
            for tweet_table in tweet_tables \
            if not cls.is_a_retweet(tweet_table)]

    @classmethod
    def is_a_retweet(cls, tweet_table):
        social_context = tweet_table.select('.tweet-social-context')
        return social_context and not 'retweet' in social_context

    @classmethod
    def extract_id(cls, tweet_table):
        tweet_div = tweet_table.select('div.tweet-text')[0]
        return tweet_div['data-id']

    @classmethod
    def extract_tweet(cls, html):
        soup = BeautifulSoup(html, 'html.parser')
        main_tweet = soup.select('table.main-tweet')[0]
        tweet_text = main_tweet.select('div.tweet-text')[0]

        tweet = Tweet()
        tweet.id = tweet_text['data-id']
        tweet.content = tweet_text.text.strip()
        tweet.timestamp = cls.convert_to_datetime(main_tweet.select('.metadata')[0].text.strip())
        return tweet

    @classmethod
    def convert_to_datetime(cls, twitter_timestamp):
        months = [
            'jan', 'feb', 'mar', 'apr',
            'mai', 'jun', 'jul', 'aug',
            'sep', 'okt', 'nov', 'des'
        ]
        for month in months:
            twitter_timestamp = twitter_timestamp.replace(month, str(months.index(month) + 1))
        return datetime.strptime(twitter_timestamp, '%H.%M - %d. %m. %Y') 
