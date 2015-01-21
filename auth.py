import os
import tweepy

consumer_key = os.environ.get('TWITTER_CONSUMER_KEY')
consumer_secret = os.environ.get('TWITTER_CONSUMER_SECRET')

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

print auth.get_authorization_url()

verifier = raw_input("VERIFIER CODE: ")

print "TOKEN/SECRET:"

print auth.get_access_token(verifier)
