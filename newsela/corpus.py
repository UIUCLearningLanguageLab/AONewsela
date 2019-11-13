import attr
from pathlib import Path
import re


@attr.s
class Corpus(object):
    version = attr.ib(validator=attr.validators.instance_of(int))
    tokens = attr.ib(validator=attr.validators.instance_of(list))
    texts = attr.ib(validator=attr.validators.instance_of(list))
    num_words = attr.ib(validator=attr.validators.instance_of(int))

    @classmethod
    def from_version(cls, version, articles_dir):

        assert version in [0, 1, 2, 3, 4, 5]

        articles_path = Path(articles_dir)
        if not articles_path.exists():
            raise FileNotFoundError(f'Did not find {articles_path}')

        print(f'Looking for articles in {articles_path}')

        words = []
        texts = []
        for path in articles_path.glob(f'*.en.{version}.txt'):
            text_in_file = path.read_text(encoding='utf-8').replace('\n', ' ')
            words_in_file = text_in_file.split()
            words.extend(words_in_file)
            texts.append(text_in_file)
        num_words = len(words)

        return cls(version, words, texts, num_words)

    @classmethod
    def from_file_name(cls, file_name, articles_dir):

        articles_path = Path(articles_dir)
        if not articles_path.exists():
            raise FileNotFoundError(f'Did not find {articles_path}')

        res = re.match(r'newsela_version(.).txt', file_name)
        assert len(res.groups()) == 1
        version = int(res.groups()[0])

        path = articles_path / file_name
        print(f'Loading corpus from {path}')
        text_in_file = path.read_text(encoding='utf-8')
        texts = text_in_file.split('\n')
        words_in_file = text_in_file.replace('\n', ' ').split()
        words = words_in_file
        num_words = len(words)

        return cls(version, words, texts, num_words)