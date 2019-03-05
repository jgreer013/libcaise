from util.file_loader import FileLoader
from pandas import DataFrame
from get_ngrams import get_ngrams
from gensim.models import LdaMulticore
from sklearn.decomposition import LatentDirichletAllocation, TruncatedSVD
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.model_selection import GridSearchCV
from pprint import pprint
import os
import gensim
import numpy as np
import guidedlda as gl
import pyLDAvis
import pyLDAvis.sklearn
import matplotlib.pyplot as plt

def main2():
    dir = "source/cpp_examples/assembly/"
    d, keys, clusters = get_ngrams(dir, n=8)
    print(len(d))

    docs = []
    for doc in d:
        if "search" in doc[0].getFilename() or "sort" in doc[0].getFilename():
            docs.append(" ".join(["_".join(x.split(" ")) for x in doc[1]]))

    vectorize = CountVectorizer(analyzer='word', min_df=1)
    dvec = vectorize.fit_transform(docs)

    lda_model = LatentDirichletAllocation(n_topics=100, max_iter=100, learning_method='online', random_state=100, batch_size=128, evaluate_every = 5,n_jobs = -1)
    lda_output = lda_model.fit_transform(dvec)

    print(lda_model)

def main():
    dir = "source/cpp_examples/assembly/"
    d, keys, clusters = get_ngrams(dir, n=8)
    print(len(d))

    docs = []
    for doc in d:
        if "sort" in doc[0].getFilename() or "search" in doc[0].getFilename():
            docs.append(doc)

    X, vocab, word_id = construct_x(docs)
    for i in range(len(vocab)):
        vocab[i] = convert_clust_to_term(vocab[i], clusters)
    print(len(clusters.keys()))
    id2word = {}
    for w in word_id:
        id2word[word_id[w]] = w

    n_topics = 13
    corpus = gensim.matutils.Dense2Corpus(X)
    print('Corpus Done')
    #model = LdaMulticore(corpus, id2word=id2word, workers=3, passes=100, alpha=0.1, eta=0.1)
    # low alpha is few words per topic
    # low eta is few topics per document
    model = gl.GuidedLDA(n_topics=n_topics, n_iter=100, random_state=7, refresh=20, alpha=0.00000001, eta=0.1)
    model.fit(X)
    topic_word = model.topic_word_
    #topic_word = model.get_topics()
    n_top_words = 3
    topic_list = []
    for i, topic_dist in enumerate(topic_word):
        topic_words = np.array(vocab)[np.argsort(topic_dist)][:-(n_top_words+1):-1]
        print('Topic {}: \n{}'.format(i, '\n'.join(topic_words)))
        topic_list.append(topic_words)
        k = np.sort(topic_dist)[:-(n_top_words+1):-1]
        #print(sum(k), k)
        print(" ")


    doc_topic = model.transform(X)
    n_top_topics = 3
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


    """
    for k in sorted(clusters.keys(), key=lambda x: int(x)):
        print(k, clusters[k])
    """




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

def convert_clust_to_term(gram, clust):
    terms = gram.split()
    for i in range(len(terms)):
        t = int(terms[i])
        if len(clust[t]) == 1:
            terms[i] = clust[t][0]
    return " ".join(terms)

main()
