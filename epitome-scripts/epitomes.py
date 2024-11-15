import os
import cltk
import re
import numpy as np
from tqdm.notebook import tqdm
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

def load_epitomes(path: str) -> tuple[list[str], list[int]]:
    """
    Loads and returns two lists from the epitomes in this order:
    load_epitomes(path) -> texts, numbers
    """

    epitome_texts = []
    epitome_numbers = []
    # we have to sort the os listdir to get the texts in alphabetical order
    for filename in sorted(os.listdir(path)):
        with open(os.path.join(path, filename), 'r', encoding='utf-8') as f:
            text = f.readlines()[-1]
            number = int(re.findall('\d+', filename)[0])
            epitome_texts.append(text)
            epitome_numbers.append(number)

    return epitome_texts, epitome_numbers

def generate_text_vectors(texts: list[str], NLP: cltk.nlp.NLP) -> tuple[list, list, list]:
    """
    Takes a list of texts as well as a cltk.NLP object to analyze the texts.
    Returns lists with POS-tags, word2vec embeddings and tokens (lemmata, actually).
    Lists are returned in this order:
    generate_text_vectors(texts, NLP) -> pos_list, emb_list, tokens_list
    """

    pos_list = []
    emb_list = []
    tokens_list = []

    for text in tqdm(texts):
        doc = NLP.analyze(text)
        pos_list.append(doc.pos)
        # word2vec embeddings, meaning we get one embedding per token per epistle
        emb_list.append(doc.embeddings)
        # use lemmata as tokens so that different conjugations are not counted separately
        tokens_list.append(doc.lemmata)

    return pos_list, emb_list, tokens_list

def token_counter(tokens_list: list[list[str]], stop_list: list[str]) -> Counter:
    """
    Takes a list of lists, each sublist containing tokens for a
    text (see medlatin.generate_text_vectors). Ignores tokens in
    stop_list. Returns a Counter object of tokens.
    """

    token_counter = {}
    for token_list in tokens_list:
        for token in token_list:
            if token not in stop_list:
                if token in token_counter:
                    token_counter[token] += 1
                else:
                    token_counter[token] = 1

    return Counter(token_counter)

def combine_pos_most_common_tokens(tokens_list: list[list[str]],
                                   pos_list:  list[list[str]],
                                   most_common_tokens: list[str]) -> list[list[str]]:
    """
    Takes a tokens_list and pos_list, each one containing sublists with tokens
    and POS-tags respectively (see medlatin.generate_text_vectors). Combines the lists
    by inserting POS-tags instead of those tokens that are NOT in the most_common_tokens.
    Returns a list with sublists for each text, each sublist containing strings that are
    either a POS-tag or a common token.
    """

    combined_pos_common_tokens = []
    for i in range(len(tokens_list)):
        pos_common_tokens = []
        for j in range(len(tokens_list[i])):
            # if the token is among the most common we just add the token
            if tokens_list[i][j] in most_common_tokens:
                pos_common_tokens.append(tokens_list[i][j])
            # if not we add its POS-tag instead
            else:
                pos_common_tokens.append(pos_list[i][j])
        combined_pos_common_tokens.append(pos_common_tokens)

    return combined_pos_common_tokens

def word_tfidf(combined_pos_tokens: list[list[str]], ngrams=2, max_feats=100):

    """
    Takes a list of lists with tokens and POS-tags combined (see
    medlatin.combine_pos_most_common_tokens). Runs sklearn's word based TF-IDF
    on those lists and returns a matrix of the shape (len(combined_pos_tokens), max_feats).
    """

    # turns the list of lists into a list of strings, which the tfidf object can work on
    combined_pos_tokens_joined = [' '.join(combined_list) for combined_list in combined_pos_tokens]

    tfidf_word = TfidfVectorizer(ngram_range=(ngrams, ngrams), max_features=max_feats, analyzer='word')

    pos_tokens_tfidf = tfidf_word.fit_transform(combined_pos_tokens_joined)

    return pos_tokens_tfidf

def char_tfidf(tokens: list[list[str]], ngrams=2, max_feats=100):

    """
    Takes a list of lists with tokens and POS-tags combined (see
    medlatin.combine_pos_most_common_tokens). Runs sklearn's character based TF-IDF
    on those lists and returns a matrix of the shape (len(tokens), max_feats).
    """

    # turns the list of lists into a list of strings which the tfidf object can work on
    tokens_joined = [' '.join(token_list) for token_list in tokens]

    tfidf_char = TfidfVectorizer(ngram_range=(ngrams, ngrams), max_features=max_feats, analyzer='char')

    char_tfidf = tfidf_char.fit_transform(tokens_joined)

    return char_tfidf