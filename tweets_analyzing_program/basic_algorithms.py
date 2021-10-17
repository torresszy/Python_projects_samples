"""
CS121: Analyzing Election Tweets (Solutions)

Algorithms for efficiently counting and sorting distinct `entities`,
or unique values, are widely used in data analysis.

Functions to implement:

- count_tokens
- find_top_k
- find_min_count
- find_most_salient

You may add helper functions.
"""

import math
from util import sort_count_pairs

def count_tokens(tokens):
    '''
    Counts each distinct token (entity) in a list of tokens

    Inputs:
        tokens: list of tokens (must be immutable)

    Returns: dictionary that maps tokens to counts
    '''

    count = {}

    for token in tokens:
        if token not in count:
            count[token] = 1
        else:
            count[token] += 1

    return count


def find_top_k(tokens, k):
    '''
    Find the k most frequently occuring tokens

    Inputs:
        tokens: list of tokens (must be immutable)
        k: a non-negative integer

    Returns: list of the top k tokens ordered by count.
    '''

    #Error checking (DO NOT MODIFY)
    if k < 0:
        raise ValueError("In find_top_k, k must be a non-negative integer")
    

    lst = sort_count_pairs(list(count_tokens(tokens).items()))[:k]
    top_k = []

    for x, y in lst:
        top_k.append(x)

    return top_k


def find_min_count(tokens, min_count):
    '''
    Find the tokens that occur *at least* min_count times

    Inputs:
        tokens: a list of tokens  (must be immutable)
        min_count: a non-negative integer

    Returns: set of tokens
    '''

    #Error checking (DO NOT MODIFY)
    if min_count < 0:
        raise ValueError("min_count must be a non-negative integer")

    count = count_tokens(tokens)
    rv = set()

    for i in count:
        if count[i] >= min_count:
            rv.add(i)

    return rv


def calculate_tf(t, doc):
    '''
    Calculate the augmented frequency of a term in a document 

    Inputs:
        t (str): a term in the document doc
        doc: a list of strings

    Returns: the augmented frequency of the term t (float)
    '''

    count = count_tokens(doc)

    if len(doc) == 0:
        tf = None
    else:
        most_freq = count[find_top_k(doc, 1)[0]]
        tf = 0.5 + 0.5 * (count[t]/most_freq)

    return tf


def calculate_idf(t, docs):
    '''
    Calculate the inverse document frequency of a term in 
      a collection of documents 

    Inputs:
        t (str): a term in the document doc
        docs: a list of lists of strings

    Returns: the inverse document frequency of the term t (float)
    '''
    N = len(docs)
    d = 0

    for doc in docs:
        if t in doc:
            d += 1    

    idf = math.log(N/d)

    return idf


def find_salient(docs, threshold):
    '''
    Compute the salient words for each document.  A word is salient if
    its tf-idf score is strictly above a given threshold.

    Inputs:
      docs: list of list of tokens
      threshold: float

    Returns: list of sets of salient words
    '''

    salient_list = []

    for doc in docs:
        salient_set = set()
        tokens = list(count_tokens(doc).keys())
        for t in tokens:
            tf_idf = calculate_tf(t, doc) * calculate_idf(t, docs)
            if tf_idf > threshold:
                salient_set.add(t)
        salient_list.append(salient_set)
        
    return salient_list
