import tweepy

class Chirp:

    def __init__(self, consumer_key, consumer_secret, access_token, access_token_secret):
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        self.api = tweepy.API(auth_handler=auth)

    def update_status(self, message):
        self.api.update_status(annoyance)
