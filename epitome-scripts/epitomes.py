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