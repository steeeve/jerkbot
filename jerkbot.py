import os
import re
import string
import tweepy
import redis
from nltk import data as nltk_data
from nltk import word_tokenize
from nltk.tag import pos_tag

update_status = True if os.getenv('UPDATE_STATUS', False) == 'TRUE' else False
ignore_previous = True if os.getenv('IGNORE_PREVIOUS', False) == 'TRUE' else False
consumer_key = os.getenv('TWITTER_CONSUMER_KEY')
consumer_secret = os.getenv('TWITTER_CONSUMER_SECRET')
access_token = os.getenv('TWITTER_ACCESS_TOKEN')
access_token_secret = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
redis_url = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')

nltk_data.path.append('./nltk_data/')

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth_handler=auth, wait_on_rate_limit=True)

r = redis.from_url(redis_url)

def untokenize(tokenized_text):
    return "".join([" "+i if not i.startswith("@") and not i.startswith("'") and i not in string.punctuation else i for i in tokenized_text]).strip()

class Jerkbot:

    def __init__(self, twitter_user):
        self.twitter_user = twitter_user

    def save_position(self, tweet_id):
        return r.set('previous_position', tweet_id)

    def previous_position(self):
        if not ignore_previous:
            return r.get('previous_position')

    def next_tweet(self):
        result = api.user_timeline(screen_name=self.twitter_user, since_id=self.previous_position(), count=1)
        if len(result) > 0:
            [tweet] = result
            self.save_position(tweet.id)
            if "@" not in tweet.text:
                return {'id': tweet.id, 'text': tweet.text}
            else:
                print "No suitable tweet."
        else:
            print "No new tweets."

    def replace_with_lego(self, tweet_text):
        tagged_tweet = pos_tag(word_tokenize(tweet_text))

        for i, (word, tag) in enumerate(tagged_tweet):
            if tag == 'NNP':
                tagged_tweet[i] = ("Lego", tag)
                break
            if tag == 'NNPS':
                tagged_tweet[i] = ("Legos", tag)
                break

        tokenized_tweet = [ word[0] for word in tagged_tweet ]

        return untokenize(tokenized_tweet)

    def cheekify(self, tweet_text):
        tweet_text = re.sub(r'([^\.]+)$', r'\1.', tweet_text)
        return "@{0}: {1} Fixed it for you.".format(self.twitter_user, tweet_text)

    def next_annoyance(self):
        tweet = self.next_tweet()
        if tweet:
            return self.cheekify(self.replace_with_lego(tweet['text']))

    def annoy(self):
        annoyance = self.next_annoyance()
        if annoyance:
            print annoyance
            if update_status:
                api.update_status(annoyance)


if __name__ == "__main__":
    j = Jerkbot('ZefTillDeath')
    j.annoy()
