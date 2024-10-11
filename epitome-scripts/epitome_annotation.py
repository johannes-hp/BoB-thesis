import cltk
import os
import pandas as pd
import numpy as np

def annotation_dataframe(text: str, cltk_nlp) -> pd.DataFrame:
    """
    Takes a text string and a cltk.NLP instance and creates a 
    DataFrame with tokens, POS-tags and an empty column for 
    annotations.
    """

    text_doc = cltk_nlp.analyze(text)
    text_df = pd.DataFrame()
    text_df['tokens'] = text_doc.tokens
    text_df['pos'] = text_doc.pos
    text_df['annotation'] = ['' for _ in range(len(text_doc.tokens))]

    return text_df

cwd = os.path.dirname(os.path.abspath(__file__))

lat_cltk = cltk.NLP(language='lat', suppress_banner=True)
lat_cltk.pipeline.processes.remove(cltk.lexicon.processes.LatinLexiconProcess)
# remove process since it slows the code (it adds definitions to each word)
lat_cltk.pipeline.processes.remove(cltk.embeddings.processes.LatinEmbeddingsProcess)
# remove process since it slows the code (it generates word2vec embeddings)

epitome_numbers = [190, 286, 432, 584, 915, 1406, 1616, 1770, 1904, 2309]

epitome_numbers = [f'e{n:04}' for n in epitome_numbers]

for epitome in epitome_numbers:
    with open(os.path.join(cwd, f'../epitomes/{epitome}.txt'), 'r', encoding='utf-8') as f:
        text = f.readlines()[-1].strip()
        text_df = annotation_dataframe(text, lat_cltk)
        text_df.to_csv(os.path.join(cwd, f'../annotation/{epitome}.csv'))