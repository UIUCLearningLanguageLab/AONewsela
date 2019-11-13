import spacy
from spacy.lang.en import English
from pathlib import Path

from newsela.corpus import Corpus

ARTICLES_DIR = '/home/ph/newsela_article_corpus_2016-01-29/articles'
OUTPUT_DIR = '/home/ph/newsela_output'

nlp = spacy.load('en_core_web_sm')
tokenizer = English().Defaults.create_tokenizer(nlp)  # tokenizer must be created this way

for version in range(6):
    c = Corpus.from_version(version, ARTICLES_DIR)
    print(f'Found {c.num_words:>9,} words for version={c.version}')

    out_path = Path(OUTPUT_DIR)
    if not out_path.exists():
        out_path.mkdir(parents=True)

    # tokenize + remove redundant whitespace + lowercase + save to file
    txt_file_name = f'newsela_version{c.version}.txt'
    f = (out_path / txt_file_name).open('w')
    for doc in tokenizer.pipe(c.texts):
        line = ' '.join([w.text.lower() for w in doc if not w.is_space])
        f.write(line + '\n')
    f.close()
