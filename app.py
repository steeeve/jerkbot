import os
import twiterator
import chirp
import jerkbot

update_status = True if os.getenv('UPDATE_STATUS', False) == 'TRUE' else False
ignore_previous = True if os.getenv('IGNORE_PREVIOUS', False) == 'TRUE' else False
twitter_user = os.getenv('TWITTER_USER')
consumer_key = os.getenv('TWITTER_CONSUMER_KEY')
consumer_secret = os.getenv('TWITTER_CONSUMER_SECRET')
access_token = os.getenv('TWITTER_ACCESS_TOKEN')
access_token_secret = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
redis_url = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')

if __name__ == "__main__":
    twiterator = twiterator.Twiterator(redis_url, consumer_key, consumer_secret, twitter_user, ignore_previous=ignore_previous)
    chirp = chirp.Chirp(consumer_key, consumer_secret, access_token, access_token_secret)
    j = jerkbot.Jerkbot(twiterator, chirp, twitter_user)
    j.annoy()
