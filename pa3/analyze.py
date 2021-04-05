"""
Analyze module
"""

import unicodedata
import sys

from basic_algorithms import find_top_k, find_min_count, find_salient

##################### DO NOT MODIFY THIS CODE #####################

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


#####################  MODIFY THIS CODE #####################


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

    typ, info, case_sen = entity_desc
    info_list = []

    for tweet in tweets:
        for i in tweet["entities"][typ]:
            if case_sen == False:
                info_list.append(i[info].lower())
            else:
                info_list.append(i[info])

    return info_list

# Task 2.1
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

    return find_top_k(collecting_entities(tweets, entity_desc), k)

    


# Task 2.2
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
    
    return find_min_count(collecting_entities(tweets, entity_desc), min_count)
    




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

    origianl_list = list(abr_text.split())
    
    final_lst = []
    for word in origianl_list:
        new_word = word.strip(PUNCTUATION)
        if new_word != "":
            if case_sensitive == False:
                new_low_word = new_word.lower()
                if stop_words_sensitive == True:
                    if new_low_word not in STOP_WORDS:
                        if new_low_word.startswith(STOP_PREFIXES) == False:
                            final_lst.append(new_low_word) 
                else:
                    if new_low_word.startswith(STOP_PREFIXES) == False:
                            final_lst.append(new_low_word)
            else:
                if stop_words_sensitive == True:
                    if new_word not in STOP_WORDS:
                        if new_word.startswith(STOP_PREFIXES) == False:
                            final_lst.append(new_word) 
                else:
                    if new_word.startswith(STOP_PREFIXES) == False:
                            final_lst.append(new_word)

    return final_lst


def collecting_abridged_text(tweets):
    '''
    collect all the abridged texts from tweets
     into a list of lists of strings

    Inputs:
        tweets: a list of tweets

    Returns: list of lists strings
    '''

    abr_text_lst = []

    for tweet in tweets:
        abr_text_lst.append(tweet["abridged_text"])

    return abr_text_lst

    
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
    ngram_lst = []
    
    # https://stackoverflow.com/questions/13423919/computing-n-grams-using-python
    for i in range(len(words_list)-n+1):
        ngram_lst.append(tuple(words_list[i:i+n]))

    return ngram_lst

    
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

    text_lst = []

    for text in collecting_abridged_text(tweets):
        tweet = Pre_processing(text, case_sensitive, stop_words_sensitive)
        text_lst += create_ngrams(n, tweet)

    return text_lst


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

    text_lst = ngram_text_list(n, tweets, case_sensitive, True)
    
    return find_top_k(text_lst, k)


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

    text_lst = ngram_text_list(n, tweets, case_sensitive, True)

    return find_min_count(text_lst, min_count)


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

    text_lst = []

    for text in collecting_abridged_text(tweets):
        tweet = Pre_processing(text, case_sensitive, False)
        text_lst.append(create_ngrams(n, tweet))

    return find_salient(text_lst,threshold)
