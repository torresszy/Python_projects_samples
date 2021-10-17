"""
Analyzing Election Tweets

Algorithms for efficiently counting and sorting distinct `entities`,
or unique values, are widely used in data analysis.

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


def find_top_k(tokens, k):
    '''
    Find the k most frequently occuring tokens

    Inputs:
        tokens: list of tokens (must be immutable)
        k: a non-negative integer

    Returns: list of the top k tokens ordered by count.
    '''


def find_min_count(tokens, min_count):
    '''
    Find the tokens that occur *at least* min_count times

    Inputs:
        tokens: a list of tokens  (must be immutable)
        min_count: a non-negative integer

    Returns: set of tokens
    '''


def calculate_tf(t, doc):
    '''
    Calculate the augmented frequency of a term in a document 

    Inputs:
        t (str): a term in the document doc
        doc: a list of strings

    Returns: the augmented frequency of the term t (float)
    '''


def calculate_idf(t, docs):
    '''
    Calculate the inverse document frequency of a term in 
      a collection of documents 

    Inputs:
        t (str): a term in the document doc
        docs: a list of lists of strings

    Returns: the inverse document frequency of the term t (float)
    '''


def find_salient(docs, threshold):
    '''
    Compute the salient words for each document.  A word is salient if
    its tf-idf score is strictly above a given threshold.

    Inputs:
      docs: list of list of tokens
      threshold: float

    Returns: list of sets of salient words
    '''