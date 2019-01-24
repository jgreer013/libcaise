from util.file_loader import FileLoader
from pandas import DataFrame
from get_ngrams import get_ngrams
import os
import numpy as np
import guidedlda as gl
from sklearn.feature_extraction.text import TfidfVectorizer

def main():
    dir = "source/cpp_examples/assembly/"
    d, keys, clusters = get_ngrams(dir, n=8)
    print(len(d))
    sort_search = []
    for i in range(len(d)):
        doc = d[i]
        fn = doc[0].getFilename()
        if "sort" in fn or "search" in fn:
            sort_search.append(i)
    d_str = [" ".join([k.replace(" ", "_") for k in doc[1]]) for doc in d]
    print(d_str[0])
    vec = TfidfVectorizer()
    X = vec.fit_transform(d_str)
    feat_names = vec.get_feature_names()
    for i in range(len(feat_names)):
        feat = feat_names[i]
        terms = feat.split("_")
        new_feat = []
        for t in terms:
            id = int(t)
            if len(clusters[id]) == 1:
                new_feat.append(clusters[id][0])
            else:
                new_feat.append(t)
        feat_names[i] = "_".join(new_feat)

    print(X.shape)

    N = 10
    features = {}
    total = 0
    for i in sort_search:
        scores = X.getrow(i).toarray()[0].ravel()
        ind = np.argsort(scores)[-1*N:][::-1]
        for k in ind:
            f = feat_names[k]
            if f not in features:
                features[f] = total
                total += 1

    for i in sort_search:
        scores = X.getrow(i).toarray()[0].ravel()
        ind = np.argsort(scores)[-1*N:][::-1]

        print(d[i][0].getFilename())
        print("Top Features: ", "  ".join([str(features[feat_names[k]]) for k in ind]))
        print("Scores: ", " ".join([str(scores[j]) for j in ind]))
        print(" ")

    for c in sorted(clusters.keys()):
        if len(clusters[c]) > 1:
            print(c, clusters[c])

    for f in features:
        print(f, features[f])


main()
