from util.file_loader import FileLoader
from pandas import DataFrame
import os
import numpy as np
import guidedlda as gl

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
    n_topics = 20
    # low alpha is few words per topic
    # low eta is few topics per document
    model = gl.GuidedLDA(n_topics=n_topics, n_iter=500, random_state=7, refresh=20, alpha=0.1, eta=0.1)
    model.fit(X)
    topic_word = model.topic_word_
    n_top_words = 3
    topic_list = []
    for i, topic_dist in enumerate(topic_word):
        topic_words = np.array(vocab)[np.argsort(topic_dist)][:-(n_top_words+1):-1]
        print('Topic {}: {}'.format(i, ' '.join(topic_words)))
        topic_list.append(topic_words)
        print(np.sort(topic_dist)[:-(n_top_words+1):-1])

    doc_topic = model.transform(X)
    n_top_topics = 3
    for i in range(doc_topic.shape[0]):
        print("Document: " + d[i][0].getFilename())
        top_topics = [np.argsort(doc_topic[i])[:-(n_top_topics+1):-1]][0]
        print("top topics: {} Document: {}".format(" ".join([str(ind) for ind in top_topics]),','.join(np.array(vocab)[list(reversed(X[i,:].argsort()))[0:5]])))
        print(np.sort(doc_topic[i])[:-(n_top_topics+1):-1])
        print(sum(np.sort(doc_topic[i])[:-(n_top_topics+1):-1]))
        for t in top_topics:
            print(topic_list[t])
        print(" ")




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
