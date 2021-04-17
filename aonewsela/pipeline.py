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

        """
        notes:
         age-ordering articles requires loading highest version first.
          (higher version -> higher simplification -> smaller grade level -> younger students)
        """

        def path_to_version(p: Path):
            return int(p.stem.split('.')[-1])

        if path_ludwig_data is None:
            path_ludwig_data = configs.Dirs.ludwig_data


        path_data = path_ludwig_data / 'AONewsela' / 'newsela_article_corpus_2016-01-29'
        print(f'Looking for articles in {path_data}')
        if not path_data.exists():
            raise FileNotFoundError(f'Did not find {path_data}.'
                                    f' Do you have access to the UIUC Language Learning Lab shared drive?')

        # search directory once, to save time
        article_paths = [p for p in path_data.rglob('*.en.*.txt')]
        if not article_paths:
            raise RuntimeError(f'Did not find any articles in {article_paths}')

        print(f'Preparing {len(article_paths)} AONewsela articles...')
        pbar = pyprind.ProgBar(len(article_paths), stream=1)

        res = []
        for path_article in sorted(article_paths, key=lambda p: path_to_version(p), reverse=True):

            # TODO many article start with a location followed by a dash - remove this

            # filter article sub-headings
            lines_filtered = []
            for line in path_article.open(encoding='utf-8').readlines():

                if line.startswith('##'):
                    continue

                if 'http' in line:  # TODO only exclude the sentence or link, not the entire line
                    continue

                if '<img' in line:
                    continue

                lines_filtered.append(line.rstrip('\n'))

            if not self.params.punctuation:
                raise NotImplementedError

            text = ' '.join(lines_filtered)
            res.append(Transcript(text.lower(), path_to_version(path_article)))

        pbar.update()

        print(f'Found {len(res)} articles', flush=True)
        assert len(res) == len(article_paths)

        return res
