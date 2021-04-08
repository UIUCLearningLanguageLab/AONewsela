from typing import List, Optional
import pyprind
from pathlib import Path

from aonewsela import configs
from aonewsela.helpers import Transcript
from aonewsela.params import NewselaParams


class Pipeline:

    def __init__(self, params=None):
        self.params = params or NewselaParams()

    def load_age_ordered_articles(self,
                                  path_ludwig_data: Optional[Path] = None,
                                  ) -> List[Transcript]:

        if path_ludwig_data is None:
            path_ludwig_data = configs.Dirs.ludwig_data

        print('Preparing AONewsela articles...')
        pbar = pyprind.ProgBar(6, stream=1)

        res = []
        for version in reversed(range(6)):  # simple first means highest version first

            articles_path = path_ludwig_data / 'AONewsela' / 'newsela_article_corpus_2016-01-29'
            print(f'Looking for articles in {articles_path}')
            if not articles_path.exists():
                raise FileNotFoundError(f'Did not find {articles_path}.'
                                        f' Do you have access to the UIUC Language Learning Lab shared drive?')

            for path in articles_path.glob(f'*.en.{version}.txt'):
                text = path.read_text(encoding='utf-8').replace('\n', ' ').lower()

                if not self.params.punctuation:
                    raise NotImplementedError

                res.append(Transcript(text, version))

            pbar.update()

        return res
