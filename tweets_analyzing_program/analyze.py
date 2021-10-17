"""
Analyze module
"""

import unicodedata
import sys

from basic_algorithms import find_top_k, find_min_count, find_salient


def keep_chr(ch):
    '''
    Find all characters that are classifed as punctuation in Unicode
    (except #, @, &) and combine them into a single string.
    '''
    return unicodedata.category(ch).startswith('P') and \
        (ch not in ("#", "@", "&"))

PUNCTUATION = " ".join([chr(i) for i in range(sys.maxunicode)
                        if keep_chr(chr(i))])

# When processing tweets, ignore these words
STOP_WORDS = ["a", "an", "the", "this", "that", "of", "for", "or",
              "and", "on", "to", "be", "if", "we", "you", "in", "is",
              "at", "it", "rt", "mt", "with"]

# When processing tweets, words w/ a prefix that appears in this list
# should be ignored.
STOP_PREFIXES = ("@", "#", "http", "&amp")


############## Part 2 ##############

def collecting_entities(tweets, entity_desc):
    '''
    Collecting the target entitites from all the tweets

    Inputs:
        tweets: a list of tweets
        entity_desc: a triple ("hashtags", "text", True),
          ("user_mentions", "screen_name", False), etc

    Returns: list of entities
    '''


def find_top_k_entities(tweets, entity_desc, k):
    '''
    Find the k most frequently occuring entitites

    Inputs:
        tweets: a list of tweets
        entity_desc: a triple ("hashtags", "text", True),
          ("user_mentions", "screen_name", False), etc
        k: integer

    Returns: list of entities
    '''    


def find_min_count_entities(tweets, entity_desc, min_count):
    '''
    Find the entitites that occur at least min_count times.

    Inputs:
        tweets: a list of tweets
        entity_desc: a triple ("hashtags", "text", True),
          ("user_mentions", "screen_name", False), etc
        min_count: integer

    Returns: set of entities
    '''


############## Part 3 ##############

def Pre_processing(abr_text, case_sensitive, stop_words_sensitive):
    '''
    pre-process the abridged text into list of strings

    Inputs:
        abr_text (str): the abridged text
        case_sensitive: boolean
        stop_words_sensitive: boolean

    Returns: list of strings
    '''


def collecting_abridged_text(tweets):
    '''
    collect all the abridged texts from tweets
     into a list of lists of strings

    Inputs:
        tweets: a list of tweets

    Returns: list of lists strings
    '''

    
def create_ngrams(n, words_list):
    '''
    return a list of pre-processed strings into
      a list of n-grams

    Inputs:
        words_list: a list of string that is 
          pre-processed
        n: integer

    Returns: list of n-grams(tuples)
    '''

    
def ngram_text_list(n, tweets, case_sensitive, stop_words_sensitive):
    '''
    take a list of abridged texts from tweets and convert 
      each text into a list of n-grams

    Inputs:
        tweets: a list of tweets
        n: integer
        case_sensitive: boolean
        stop_words_sensitive: boolean

    Returns: list of lists of n-grams(tuples)
    '''


def find_top_k_ngrams(tweets, n, case_sensitive, k):
    '''
    Find k most frequently occurring n-grams

    Inputs:
        tweets: a list of tweets
        n: integer
        case_sensitive: boolean
        k: integer

    Returns: list of n-grams
    '''


def find_min_count_ngrams(tweets, n, case_sensitive, min_count):
    '''
    Find n-grams that occur at least min_count times.

    Inputs:
        tweets: a list of tweets
        n: integer
        case_sensitive: boolean
        min_count: integer

    Returns: set of n-grams
    '''


def find_salient_ngrams(tweets, n, case_sensitive, threshold):
    '''
    Find the salient n-grams for each tweet.

    Inputs:
        tweets: a list of tweets
        n: integer
        case_sensitive: boolean
        threshold: float

    Returns: list of sets of strings
    '''