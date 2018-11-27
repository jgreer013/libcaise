from hlda.sampler import HierarchicalLDA
from util.file_loader import FileLoader
from pandas import DataFrame
import os
import numpy as np

def main():
    fl = FileLoader()
    dir = "source/cpp_examples/assembly/"
    files = os.listdir(dir)
    asm_files = []
    for f in files:
        if f[-8:] == "only.txt":
            fl.addFilename(dir + f)

    d = fl.getData(type=np.dtype('unicode_'))
    X, vocab, word_id = construct_corpus(d)
    n_topics = 20

    n_samples = 500       # no of iterations for the sampler
    alpha = 0.1           # smoothing over level distributions/
    gamma = 1.0           # CRP smoothing parameter; number of imaginary customers at next, as yet unused table
    eta = 0.1             # smoothing over topic-word distributions
    num_levels = 2        # the number of levels in the tree
    display_topics = 50   # the number of iterations between printing a brief summary of the topics so far
    n_words = 5           # the number of most probable words to print for each topic after model estimation
    with_weights = True
    hlda = HierarchicalLDA(X, vocab, alpha=alpha, gamma=gamma, eta=eta, num_levels=num_levels)
    hlda.estimate(n_samples, display_topics=display_topics, n_words=n_words, with_weights=with_weights)

def construct_corpus(d):
    uni = set()
    docs = []
    for data in d:
        uni.update(data[1])
        docs.append(data[1])
    vocab = sorted(list(uni))
    word_to_id = dict((w, id) for id, w in enumerate(vocab))
    corpus = [[0 for word in doc] for doc in docs]
    for r in range(len(corpus)):
        doc = docs[r]
        for c in range(len(corpus[r])):
            word = doc[c]
            corpus[r][c] = word_to_id[word]

    return corpus, vocab, word_to_id

def construct_x(d):
    uni = set()
    docs = []
    for data in d:
        uni.update(data[1])
        docs.append(data[1])
    vocab = sorted(list(uni))
    word_to_id = dict((w, id) for id, w in enumerate(vocab))
    X = np.zeros(shape=(len(d), len(vocab)), dtype='int64')
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
