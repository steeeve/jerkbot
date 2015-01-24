import mangle

class Jerkbot:

    def __init__(self, twiterator, chirp, twitter_user, update_status=False):
        self.twiterator = twiterator
        self.chirp = chirp
        self.twitter_user = twitter_user
        self.update_status = update_status

    def annoy(self):
        tweet = self.twiterator.next_tweet()
        print '[FETCHED TWEET] {0}'.format(tweet['text'])
        if tweet and not '@' in tweet['text']:
            status = mangle.replace_with_lego(tweet['text'])
            status = mangle.fixed_it_for_you(self.twitter_user, status)
            print '[MANGLED TWEET] {0}'.format(status)
            if self.update_status:
                self.chirp.update_status(status)
                print '[SENT MANGLED TWEET]'
        else:
            print '[TWEET NOT SUITABLE FOR MANGLING]'
