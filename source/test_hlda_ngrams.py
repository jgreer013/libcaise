from hlda.sampler import HierarchicalLDA
from util.file_loader import FileLoader
from pandas import DataFrame
from get_ngrams import get_ngrams
import os
import numpy as np

def main():
    dir = "source/cpp_examples/dynamic_only/"
    d, keys, clusters = get_ngrams(dir, n=8)

    docs = []
    for doc in d:
        if "sort" in doc[0].getFilename() or "search" in doc[0].getFilename():
            docs.append(doc)

    X, vocab, word_id = construct_corpus(docs)
    for i in range(len(vocab)):
        vocab[i] = convert_clust_to_term(vocab[i], clusters)
    print(len(docs))

    n_samples = 500       # no of iterations for the sampler
    alpha = 10.0           # smoothing over level distributions/
    gamma = 1.0           # CRP smoothing parameter; number of imaginary customers at next, as yet unused table
    eta = 0.1             # smoothing over topic-word distributions
    num_levels = 3        # the number of levels in the tree
    display_topics = 50   # the number of iterations between printing a brief summary of the topics so far
    n_words = 5           # the number of most probable words to print for each topic after model estimation
    with_weights = True
    hlda = HierarchicalLDA(X, vocab, alpha=alpha, gamma=gamma, eta=eta, num_levels=num_levels)
    hlda.estimate(n_samples, display_topics=display_topics, n_words=n_words, with_weights=with_weights)

    #for c in sorted(clusters.keys(), key=lambda x: int(x)):
    #    print(c, clusters[c])

    leaves = hlda.document_leaves
    for doc in sorted(leaves.keys(), key=lambda x:leaves[x].node_id):
        print("\t", leaves[doc].node_id, "\t", docs[doc][0].getFilename())

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

def convert_clust_to_term(gram, clust):
    terms = gram.split()
    for i in range(len(terms)):
        t = int(terms[i])
        if len(clust[t]) == 1:
            terms[i] = clust[t][0]
    return " ".join(terms)


main()
