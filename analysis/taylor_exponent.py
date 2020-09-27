import numpy as np
from collections import Counter
from scipy import optimize
import matplotlib.pyplot as plt

from newsela.corpus import Corpus

ARTICLES_DIR = '/home/ph/Dropbox/newsela_output'
NUM_VERSIONS = 5
SPLIT_SIZE = 5620
PLOT_FIT = True


def fitfunc(p, x):
    return p[0] + p[1] * x


def errfunc(p, x, y):
    return y - fitfunc(p, x)


for version in range(NUM_VERSIONS):
    c = Corpus.from_file_name(f'newsela_version{version}.txt', articles_dir=ARTICLES_DIR)
    types = set(c.tokens)
    w2i = {w: n for n, w in enumerate(types)}
    token_ids = [w2i[t] for t in c.tokens]

    # make freq_mat
    num_splits = c.num_tokens // SPLIT_SIZE + 1
    num_types = len(types)
    freq_mat = np.zeros((num_types, num_splits))
    start_locs = np.arange(0, c.num_tokens, SPLIT_SIZE)
    num_start_locs = len(start_locs)
    for split_id, start_loc in enumerate(start_locs):
        for token_id, f in Counter(token_ids[start_loc:start_loc + SPLIT_SIZE]).items():
            freq_mat[token_id, split_id] = f
    # x, y
    freq_mat = freq_mat[~np.all(freq_mat == 0, axis=1)]
    x = freq_mat.mean(axis=1)  # make sure not to have rows with zeros
    y = freq_mat.std(axis=1)
    # fit
    pinit = np.array([1.0, -1.0])
    logx = np.log10(x)
    logy = np.log10(y)
    out = optimize.leastsq(errfunc, pinit, args=(logx, logy), full_output=True)

    for i in out:
        print(i)

    pfinal = out[0]
    amp = pfinal[0]
    alpha = pfinal[1]
    # fig
    fig, ax = plt.subplots(figsize=(6, 6), dpi=163)
    plt.title(f'Newsela\nversion {version + 1} of {NUM_VERSIONS}')
    ax.set_xlabel('mean')
    ax.set_ylabel('std')
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.tick_params(axis='both', which='both', top=False, right=False)
    # plot
    ax.text(x=1.0, y=0.3, s='Taylor\'s exponent: {:.3f}'.format(alpha))
    ax.loglog(x, y, '.', markersize=2)
    if PLOT_FIT:
        ax.loglog(x, amp * (x ** alpha) + 0, '.', markersize=2)  # TODO test
    plt.show()






