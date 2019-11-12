

from newsela.corpus import Corpus

ARTICLES_DIR = '/home/ph/newsela_article_corpus_2016-01-29/articles'

for level in range(5):
    c = Corpus.from_level(level, ARTICLES_DIR)
    print(f'Found {c.num_words:>9,} for level={c.level}')