from twitter import *
from tweet import Tweet
from user import User
import os

class OAuthSettings:
	app_name = "Emergency Services Norway"

	def __init__(self):
		self.get_user_credentials()

	def get_user_credentials(self):
		self.get_app_credentials()
		app_credential_file = os.path.expanduser('~/.my_app_credentials')
		if not os.path.exists(app_credential_file):
		    oauth_dance(self.app_name, self.consumer_key, self.consumer_secret, app_credentials)
		self.oauth_token, self.oauth_secret = read_token_file(app_credential_file)

	def get_app_credentials(self):
		user_credential_file = os.path.expanduser('~/.my_user_credentials')

		if not os.path.exists(user_credential_file):
			raise NameError('App consumer keys are missing.')
		self.consumer_key, self.consumer_secret = read_token_file(user_credential_file)

	def get_oauth_settings(self):
		return OAuth(
		    consumer_key=self.consumer_key,
		    consumer_secret=self.consumer_secret,
		    token=self.oauth_token,
		    token_secret=self.oauth_secret
		)

class TwitterListener:

	def __init__(self):
		self.authSettings = OAuthSettings()

	def listen_to_twitter(self):
		twitter_stream = TwitterStream(auth=self.authSettings.get_oauth_settings(), domain="userstream.twitter.com")

		for twitter_object in twitter_stream.user():
			try:
				tweet = Tweet()
				tweet.user = User(twitter_object['user']['name'])
				tweet.id = twitter_object['id_str']
				tweet.content = twitter_object['text']
				tweet.timestamp = twitter_object['timestamp_ms']
				print(tweet)
			except KeyError:
				# We encoutered something other than a tweet, moving on. 
				pass 

if __name__ == '__main__':
    listener = TwitterListener()
    listener.listen_to_twitter()
