from util.file_loader import FileLoader
from pandas import DataFrame
from get_ngrams import get_ngrams
from gensim.models import LdaMulticore
import os
import gensim
import numpy as np
import guidedlda as gl

def main():
    dir = "source/cpp_examples/assembly/"
    d, keys, clusters = get_ngrams(dir, n=5)
    print(len(d))

    X, vocab, word_id = construct_x(d)
    print(len(clusters.keys()))
    id2word = {}
    for w in word_id:
        id2word[word_id[w]] = w

    n_topics = len(X) // 16
    corpus = gensim.matutils.Dense2Corpus(X)
    print('Corpus Done')
    model = LdaMulticore(corpus, id2word=id2word, workers=3, passes=100, alpha=0.1, eta=0.1)
    # low alpha is few words per topic
    # low eta is few topics per document
    #model = gl.GuidedLDA(n_topics=n_topics, n_iter=100, random_state=7, refresh=20, alpha=0.1, eta=0.1)
    #model.fit(X)
    #topic_word = model.topic_word_
    topic_word = model.get_topics()
    n_top_words = 3
    topic_list = []
    for i, topic_dist in enumerate(topic_word):
        topic_words = np.array(vocab)[np.argsort(topic_dist)][:-(n_top_words+1):-1]
        print('Topic {}: {}'.format(i, ' '.join(topic_words)))
        topic_list.append(topic_words)
        print(np.sort(topic_dist)[:-(n_top_words+1):-1])

    """
    doc_topic = model.transform(X)
    n_top_topics = 3
    for i in range(doc_topic.shape[0]):
        fn = d[i][0].getFilename()
        if "sort" in fn or "search" in fn:
            print("Document: " + fn)
            top_topics = [np.argsort(doc_topic[i])[:-(n_top_topics+1):-1]][0]
            print("top topics: {} Document: {}".format(" ".join([str(ind) for ind in top_topics]),', '.join(np.array(vocab)[list(reversed(X[i,:].argsort()))[0:5]])))
            print(np.sort(doc_topic[i])[:-(n_top_topics+1):-1])
            print(sum(np.sort(doc_topic[i])[:-(n_top_topics+1):-1]))
            for t in top_topics:
                print(topic_list[t])
            print(" ")
    """

    for k in sorted(clusters.keys(), key=lambda x: int(x)):
        print(k, clusters[k])




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
