from util.file_loader import FileLoader
from pandas import DataFrame
from get_ngrams import get_ngrams
import os
import gensim
import numpy as np
import guidedlda as gl
import matplotlib.pyplot as plt

subs, dir = "static_small", "source/cpp_examples/assembly/"
#subs, dir = "static_large", "source/cpp_examples/assembly/"
#subs, dir = "dynamic", "source/cpp_examples/dynamic_only/"
#subs, dir = "dynamic_nol", "source/cpp_examples/dynamic_only_no_library/"

def main():
    subs, dir = "static_small", "source/cpp_examples/assembly/"
    d, keys, clusters = get_ngrams(dir, subs, n=8, use_pickle=False)

    docs = d

    X, vocab, word_id = construct_x(docs)

    for i in range(len(vocab)):
        vocab[i] = convert_clust_to_term(vocab[i], clusters)

    id2word = {}
    for w in word_id:
        id2word[word_id[w]] = w

    n_topics = 13
    corpus = gensim.matutils.Dense2Corpus(X)
    print('Corpus Done')

    # low alpha means you want few words per topic
    # low eta means you want few topics per document
    al = 0.00000001
    #al = 0.1
    model = gl.GuidedLDA(n_topics=n_topics, n_iter=100, random_state=7, refresh=20, alpha=al, eta=0.1)
    model.fit(X)
    topic_word = model.topic_word_
    n_top_words = 3
    topic_list = []

    # Print topics
    for i, topic_dist in enumerate(topic_word):
        topic_words = np.array(vocab)[np.argsort(topic_dist)][:-(n_top_words+1):-1]
        print('Topic {}: \n{}'.format(i, '\n'.join(topic_words)))
        topic_list.append(topic_words)
        k = np.sort(topic_dist)[:-(n_top_words+1):-1]
        print(k)
        print(" ")


    doc_topic = model.transform(X)
    n_top_topics = 5

    # Print Documents
    for i in range(doc_topic.shape[0]):
        fn = docs[i][0].getFilename()
        if "sort" in fn or "search" in fn:
            print("Document: " + fn)
            top_topics = [np.argsort(doc_topic[i])[:-(n_top_topics+1):-1]][0]
            print("top topics: {} Document: {}".format(" ".join([str(ind) for ind in top_topics]),', '.join(np.array(vocab)[list(reversed(X[i,:].argsort()))[0:5]])))
            print(np.sort(doc_topic[i])[:-(n_top_topics+1):-1])
            print(sum(np.sort(doc_topic[i])[:-(n_top_topics+1):-1]))
            #for t in top_topics:
            #    print(topic_list[t])
            print(" ")


    # Print clusters
    for k in sorted(clusters.keys(), key=lambda x: int(x)):
        print(k, clusters[k])


# Construct frequency matrix, vocab list, and word-id dict
def construct_x(d):
    uni = set()
    docs = []
    for data in d:
        uni.update(data[1])
        docs.append(data[1])
    vocab = sorted(list(uni))
    word_to_id = dict((w, id) for id, w in enumerate(vocab))
    X = np.zeros(shape=(len(docs), len(vocab)), dtype='uint16')
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

# Converts cluster id to term(s)
def convert_clust_to_term(gram, clust):
    terms = gram.split()
    for i in range(len(terms)):
        t = int(terms[i])
        if len(clust[t]) == 1: # 1 term
            terms[i] = clust[t][0]
        elif len(clust[t]) == 2: # 2 terms
            terms[i] = "/".join(clust[t][:2])
    return " ".join(terms)

main()
