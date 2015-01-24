import tweepy
import redis

class Twiterator:

    def __init__(self, redis_url, consumer_key, consumer_secret, twitter_user, ignore_previous=False):
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        self.api = tweepy.API(auth_handler=auth)
        self.r = redis.from_url(redis_url)
        self.twitter_user = twitter_user
        self.ignore_previous = ignore_previous

    def save_position(self, tweet_id):
        return self.r.set('previous_position', tweet_id)

    def previous_position(self):
        if not self.ignore_previous:
            return self.r.get('previous_position')

    def next_tweet(self):
        result = self.api.user_timeline(screen_name=self.twitter_user, since_id=self.previous_position(), count=1)
        if len(result) > 0:
            [tweet] = result
            self.save_position(tweet.id)
            return {'id': tweet.id, 'text': tweet.text}
