import os
import cltk
from tqdm.notebook import tqdm
from collections import Counter

def load_medlatin(path: str) -> tuple[list[str], list[str], list[str]]:
    """
    Loads and returns three lists from the MedLatin texts in this order:
    load_medlatin(path) -> texts, authors, titles
    """

    medlatin_texts = []
    medlatin_authors = []
    medlatin_titles = []
    # we have to sort the os listdir to get the texts in alphabetical order
    for filename in sorted(os.listdir(path)):
        with open(os.path.join(path, filename), 'r', encoding='utf-8') as f:
            text = f.read()
            author, title = filename.split('_')
            medlatin_texts.append(text)
            medlatin_authors.append(author)
            medlatin_titles.append(title)

    return medlatin_texts, medlatin_authors, medlatin_titles

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

def token_counter(tokens_list: list[list[str]]) -> Counter:
    """
    Takes a list of lists, each sublist containing tokens for a 
    text (see medlatin.generate_text_vectors). Returns a Counter 
    object of tokens.
    """

    token_counter = {}
    for token_list in tokens_list:
        for token in token_list:
            if token in token_counter:
                token_counter[token] += 1
            else:
                token_counter[token] = 1

    return Counter(token_counter)

def get_common_tokens(tokens_counter: Counter, n=20, stop_list=[]) -> list[str]:
    """
    Takes a counter of tokens (see medlatin.token_counter) and finds 
    the n (default 20) most common tokens. Ignores token strings provided 
    in the stop_list (default empty). Returns a list of the n most common 
    tokens in descending order.
    """

    most_common_result = []
    most_common_counter = tokens_counter.most_common()
    i = 0
    while len(most_common_result) < n:
        token = most_common_counter[i][0]
        if token not in stop_list:
            most_common_result.append(token)
        i += 1

    return most_common_result

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