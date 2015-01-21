import os
import re
import string
import tweepy
import redis
from nltk import word_tokenize
from nltk.tag import pos_tag

consumer_key = os.environ.get('TWITTER_CONSUMER_KEY')
consumer_secret = os.environ.get('TWITTER_CONSUMER_SECRET')
access_token = os.environ.get('TWITTER_ACCESS_TOKEN')
access_token_secret = os.environ.get('TWITTER_ACCESS_TOKEN_SECRET')
redis_host = os.environ.get('REDIS_HOST')
redis_port = os.environ.get('REDIS_PORT')

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth_handler=auth, wait_on_rate_limit=True)
r = redis.StrictRedis(host=redis_host, port=redis_port)

def untokenize(tokenized_text):
    return "".join([" "+i if not i.startswith("'") and i not in string.punctuation else i for i in tokenized_text]).strip()

class Jerkbot:

    def __init__(self, twitter_user):
        self.twitter_user = twitter_user

    def save_position(self, tweet_id):
        return r.set('previous_position', tweet_id)

    def previous_position(self):
        return None
        return r.get('previous_position')

    def next_tweet(self):
        result = api.user_timeline(screen_name=self.twitter_user, since_id=self.previous_position(), count=1)
        if len(result) > 0:
            [tweet] = result
            self.save_position(tweet.id)
            return {'id': tweet.id, 'text': tweet.text}

    def replace_with_lego(self, tweet_text):
        tagged_tweet = pos_tag(word_tokenize(tweet_text))

        for i, (word, tag) in enumerate(tagged_tweet):
            if tag == 'NNP' or tag == 'NNPS':
                tagged_tweet[i] = ("Lego", tag)
                break

        tokenized_tweet = [ word[0] for word in tagged_tweet ]

        return untokenize(tokenized_tweet)

    def cheekify(self, tweet_text):
        tweet_text = re.sub(r'([^\.]+)$', r'\1.', tweet_text)
        return "@{0}: {1} Fixed it for you.".format(self.twitter_user, tweet_text)

    def next_annoyance(self):
        tweet = self.next_tweet()
        return self.cheekify(self.replace_with_lego(tweet['text']))

    def annoy(self):
        next_annoyance = self.next_annoyance()
        print next_annoyance
        api.update_status(next_annoyance)


if __name__ == "__main__":
    j = Jerkbot('ZefTillDeath')
    j.annoy()
