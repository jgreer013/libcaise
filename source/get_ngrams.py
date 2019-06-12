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

def load_files(subsc, dir):
    fl = FileLoader(use_clust=True, clust_name = "clusters_" + subsc + ".txt")
    files = os.listdir(dir)
    for f in files:
        if f[-8:] == "only.txt":
            if subsc == "static_small":
                if "search" in f or "sort" in f:
                    fl.addFilename(dir + f)
            else:
                fl.addFilename(dir + f)
    d = fl.getData(type=np.dtype('unicode_'))
    return d, fl.clusters, fl.key

def get_ngrams(dir, subscript, n=3, use_pickle=True):
    if use_pickle:
        try:
            with open("ngram_pickle_" + subscript + str(n) + ".obj", 'rb') as f:
                ng = pickle.load(f)
            print("Data successfully loaded from pickle")
        except:
            d = load_files(subscript, dir)
            clust = fl.clusters
            keys = fl.key

            sentences = []
            for i in range(len(d)):
                data = d[i]
                s = list(data[1])
                d[i][1] = list(map(" ".join, ngrams(s, n)))
            ng = Ngram_data(d, clust, keys)
            with open("ngram_pickle_" + subscript + str(n) + ".obj", 'wb') as f:
                pickle.dump(ng, f)
            print("Pickling Complete")
            return get_ngrams(dir, subscript, n)
    else:
        d, clust, keys = load_files(subscript, dir)

        sentences = []
        for i in range(len(d)):
            data = d[i]
            s = list(data[1])
            d[i][1] = list(map(" ".join, ngrams(s, n)))
        ng = Ngram_data(d, clust, keys)

    return ng.d, ng.keys, ng.clust
