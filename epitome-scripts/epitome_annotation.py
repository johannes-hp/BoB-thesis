import cltk
import os
import pandas as pd

cwd = os.path.dirname(os.path.abspath(__file__))

lat_cltk = cltk.NLP(language='lat', suppress_banner=True)
lat_cltk.pipeline.processes.remove(cltk.lexicon.processes.LatinLexiconProcess)
# remove process since it slows the code (it adds definitions to each word)
lat_cltk.pipeline.processes.remove(cltk.embeddings.processes.LatinEmbeddingsProcess)
# remove process since it slows the code (it generates word2vec embeddings)

with open(os.path.join(cwd, '../epitomes/e0190.txt'), 'r', encoding='utf-8') as f:
     text190 = f.readlines()[-1].strip()

with open(os.path.join(cwd, '../epitomes/e0432.txt'), 'r', encoding='utf-8') as f:
    text432 = f.readlines()[-1].strip()

with open(os.path.join(cwd, '../epitomes/e1904.txt'), 'r', encoding='utf-8') as f:
    text1904 = f.readlines()[-1].strip()

text190_doc = lat_cltk.analyze(text190)
text432_doc = lat_cltk.analyze(text432)
text1904_doc = lat_cltk.analyze(text1904)

text190_df = pd.DataFrame()
text190_df['tokens'] = text190_doc.tokens
text190_df['pos'] = text190_doc.pos

text432_df = pd.DataFrame()
text432_df['tokens'] = text432_doc.tokens
text432_df['pos'] = text432_doc.pos

text1904_df = pd.DataFrame()
text1904_df['tokens'] = text1904_doc.tokens
text1904_df['pos'] = text1904_doc.pos

text190_df.to_csv(os.path.join(cwd, '../annotation/e0190.csv'))
text432_df.to_csv(os.path.join(cwd, '../annotation/e0432.csv'))
text1904_df.to_csv(os.path.join(cwd, '../annotation/e1904.csv'))