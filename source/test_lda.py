from util.file_loader import FileLoader
from pandas import DataFrame
import os
import numpy as np
import guidedlda

def main():
    fl = FileLoader()
    dir = "source/cpp_examples/assembly/"
    files = os.listdir("source/cpp_examples/assembly/")
    asm_files = []
    for f in files:
        if f[-8:] == "only.txt":
            fl.addFilename(dir + f)

    d = fl.getData(type=np.dtype('unicode_'))
    X, vocab, word_id = construct_x(d)
    print(x)
    print(vocab)
    print(word_id)


def construct_x(d):
    uni = set()
    docs = []
    for data in d:
        uni.update(data[1])
        docs.append(data[1])
    vocab = sorted(list(uni))
    word_id = dict((w, id) for id, w in enumerate(vocab))
    X = np.zeros(len(d), len(vocab))
    for r in range(len(X)):
        counts = {}
        doc = docs[r]
        for w in doc:
            if w in counts:
                counts[w] += 1
            else:
                counts[w] = 1

        for c in range(len(vocab)):
            if word_id[c] in counts:
                X[r][c] = counts[word_id[c]]
            else:
                X[r][c] = 0

    return X, vocab, word_id

main()
