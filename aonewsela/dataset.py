
from typing import Set, List, Optional, Tuple
from functools import reduce
from operator import iconcat

from aonewsela.params import NewselaParams
from aonewsela.pipeline import Pipeline
from aonewsela.helpers import Transcript


def tokens_from_transcripts(transcripts: List[str],
                            ) -> List[str]:
    tokenized_transcripts = [d.split() for d in transcripts]
    tokens = reduce(iconcat, tokenized_transcripts, [])  # flatten list of lists
    return tokens


class NewselaDataSet:
    def __init__(self,
                 params: Optional[NewselaParams] = None,
                 ):

        if params is None:
            params = NewselaParams()

        self.pipeline = Pipeline(params)
        self.transcripts: List[Transcript] = self.pipeline.load_age_ordered_articles()

    def load_transcripts(self) -> List[str]:
        res = [t.text for t in self.transcripts]
        return res

    def load_tokens(self) -> List[str]:
        res = tokens_from_transcripts([t.text for t in self.transcripts])
        return res

    def load_sentences(self) -> List[str]:

        exceptions = {'u.s.', 'u.n.', 'st.', 'dr.', 'd.c.', 'jan.', 'feb.'}

        sentences = []
        tokens_in_sentence = []
        for token in self.load_tokens():
            if (token.endswith('.') or token.endswith('!') or token.endswith('?')) and token not in exceptions:
                # separate punctuation from sentence with whitespace
                punctuation = token[-1]
                sentence = ' '.join(tokens_in_sentence) + ' ' + token[:-1] + ' ' + punctuation
                sentences.append(sentence)
                tokens_in_sentence = []
            else:
                tokens_in_sentence.append(token)

        return sentences

    def load_text(self) -> str:
        return ' '.join(self.load_tokens())
