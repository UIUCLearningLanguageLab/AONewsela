from tabulate import tabulate
from pathlib import Path

from wordplay.measures import calc_selectivity
from wordplay.representation import make_context_by_term_matrix

from newsela.corpus import Corpus

ARTICLES_DIR = '/home/ph/Dropbox/newsela_output'
CONTEXT_SIZE = 3
PROBES_NAME = 'syn-4096'
CORPUS_NAME = 'childes-20180319'
NUM_VERSIONS = 5

nouns = set(Path('nouns_for_selectivity.txt').read_text().split('\n'))
print(nouns)


version2y = {}
version2cttr_chance = {}
version2cttr_observed = {}
for version in range(NUM_VERSIONS):
    c = Corpus.from_file_name(f'newsela_version{version}.txt', articles_dir=ARTICLES_DIR)

    # co-occurrence matrix
    tw_mat_observed, xws_observed, _ = make_context_by_term_matrix(c.tokens,
                                                                   context_size=CONTEXT_SIZE,
                                                                   shuffle_tokens=False)
    tw_mat_chance, xws_chance, _ = make_context_by_term_matrix(c.tokens,
                                                               context_size=CONTEXT_SIZE,
                                                               shuffle_tokens=True)

    # calc selectivity of noun contexts
    cttr_chance, cttr_observed, y = calc_selectivity(tw_mat_chance,
                                                     tw_mat_observed,
                                                     xws_chance,
                                                     xws_observed,
                                                     nouns)
    print(f'version={version} selectivity={y}')
    print()

    version2cttr_chance[version] = cttr_chance
    version2cttr_observed[version] = cttr_observed
    version2y[version] = y

# latex table - aggregated
headers = ['Simplification', 'CTTR-observed', 'CTTR-chance', 'NOUN-context selectivity']
rows = [
    (version, version2cttr_chance[version], version2cttr_observed[version], version2y[version])
    for version in range(NUM_VERSIONS)
]
print(tabulate(rows,
               headers=headers,
               tablefmt='latex',
               floatfmt=".4f"))