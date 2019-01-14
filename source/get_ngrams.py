from util.file_loader import FileLoader
from pandas import DataFrame
import os
import numpy as np
from nltk.util import ngrams


def get_ngrams(dir, n=3):
    fl = FileLoader(use_clust=True)
    files = os.listdir(dir)
    for f in files:
        if f[-8:] == "only.txt":
            fl.addFilename(dir + f)

    d = fl.getData(type=np.dtype('unicode_'))
    clust = fl.clusters
    keys = fl.key
    sentences = []
    for i in range(len(d)):
        data = d[i]
        s = list(data[1])
        d[i][1] = list(map(" ".join, ngrams(s, n)))

    return d, keys, clust
