from util.file_loader import FileLoader
from pandas import DataFrame
from get_ngrams import get_ngrams
from gensim.models import LdaMulticore
import os
import gensim
import numpy as np

def main():
    fn = "assembly"
    dir = "source/cpp_examples/assembly/"
    d, keys, clusters = get_ngrams(dir, n=5)
    print(len(d))

    X, vocab, word_id = construct_x(d)
    id2word = {}
    for w in word_id:
        id2word[word_id[w]] = w

    with open("vocab." + fn + ".txt", 'w') as f:
        for id in id2word:
            f.write(id2word[id].replace(" ","_") + "\n")

    with open("docword." + fn + ".txt", 'w') as f:
        f.write(str(len(d)) + "\n")
        f.write(str(len(vocab)) + "\n")
        f.write(str(np.count_nonzero(X)) + "\n")
        for i in range(len(X)):
            for j in range(len(X[i])):
                if X[i,j] != 0:
                    f.write(str(i+1) + " " + str(j+1) + " " + str(X[i,j]) + "\n")




def construct_x(d):
    uni = set()
    docs = []
    for data in d:
        uni.update(data[1])
        docs.append(data[1])
    vocab = sorted(list(uni))
    word_to_id = dict((w, id) for id, w in enumerate(vocab))
    X = np.zeros(shape=(len(d), len(vocab)), dtype='uint16')
    for r in range(len(X)):
        counts = {}
        doc = docs[r]
        for w in doc:
            wid = word_to_id[w]
            if wid in counts:
                counts[wid] += 1
            else:
                counts[wid] = 1

        for c in range(len(vocab)):
            if word_to_id[vocab[c]] in counts:
                X[r][c] = counts[c]
            else:
                X[r][c] = 0

    return X, vocab, word_to_id

main()
