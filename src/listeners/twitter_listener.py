from twitter import *
from tweet.tweet import Tweet
from user.user import User
from config import configuration as config 
import os

class OAuthSettings:
	app_name = "Emergency Services Norway"

	def get_oauth_settings(self):
		return OAuth(
		    consumer_key=config['twitter']['consumer_key'],
		    consumer_secret=config['twitter']['consumer_secret'],
		    token=config['twitter']['oauth_token'],
		    token_secret=config['twitter']['oauth_secret']
		)

class TwitterListener:

	def __init__(self):
		self.authSettings = OAuthSettings()

	def listen_to_twitter(self, parent_process):
		twitter_stream = TwitterStream(auth=self.authSettings.get_oauth_settings(), domain="userstream.twitter.com")

		print("Opened twitter stream")

		for twitter_object in twitter_stream.user():
			try:
				# Extract info from the tweet
				tweet = Tweet()
				tweet.user = User(twitter_object['user']['name'])
				tweet.id = twitter_object['id_str']
				tweet.content = twitter_object['text']
				tweet.timestamp = twitter_object['timestamp_ms']

				# Send the tweet to the parent process (web socket)
				parent_process.send(tweet)
			except (KeyError, TypeError) as e:
				# We encoutered something other than a tweet, moving on. 
				pass 

