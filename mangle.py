import re
import string
from nltk import data as nltk_data
from nltk import word_tokenize
from nltk.tag import pos_tag

nltk_data.path.append('./nltk_data/')

def untokenize(tokenized_text):
    glued_text = "".join([" "+i for i in tokenized_text]).strip()
    glued_text = re.sub(r'\s([!?,./])', r'\1', glued_text)
    glued_text = re.sub(r'\s?([\'@])\s?', r'\1', glued_text)
    glued_text = re.sub(r'([#`;:])\s?', r'\1', glued_text)
    return glued_text

def replace_with_lego(tweet_text):
    tagged_tweet = pos_tag(word_tokenize(tweet_text))

    for i, (word, tag) in enumerate(tagged_tweet):
        if i > 0 and tagged_tweet[i-1][0] != '@':
            print tagged_tweet[i-1]
            if tag in ['NN', 'NNP']:
                tagged_tweet[i] = ('Lego', tag)
            if tag in ['NNS', 'NNPS']:
                tagged_tweet[i] = ('Legos', tag)

    tokenized_tweet = [ word[0] for word in tagged_tweet ]

    return untokenize(tokenized_tweet)

def fixed_it_for_you(twitter_user, tweet_text):
    tweet_text = re.sub(r'([^\.]+)$', r'\1.', tweet_text)
    return "@{0}: {1} There, fixed it for you.".format(twitter_user, tweet_text)
