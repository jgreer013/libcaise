from util.file_loader import FileLoader
from pandas import DataFrame
import os
import numpy as np
from nltk.util import ngrams
import pickle

class Ngram_data:
    def __init__(self, d, c, k):
        self.d = d
        self.clust = c
        self.keys = k


def get_ngrams(dir, subscript, n=3):
    try:
        with open("ngram_pickle" + subscript + str(n) + ".obj", 'rb') as f:
            ng = pickle.load(f)
        print("Data successfully loaded from pickle")
    except:
        print(subscript)
        fl = FileLoader(use_clust=True, clust_name="clusters"+subscript+".txt")
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
        ng = Ngram_data(d, clust, keys)
        with open("ngram_pickle" + subscript + str(n) + ".obj", 'wb') as f:
            pickle.dump(ng, f)
        print("Pickling Complete")
        return get_ngrams(dir, subscript, n)

    return ng.d, ng.keys, ng.clust
