from util.file_loader import FileLoader
from pandas import DataFrame
from matplotlib import pyplot as plt
import os
import numpy as np
from gensim.models import Word2Vec
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster
import pickle

# Get word2vec data
# <uniques> is unique terms
# <sentences> is the list of sentences in document
# <size> is dimensionality of word vectors
# <window> is number of words in Word2Vec window
def word_vec(uniques, sentences, size=500, window=5):
    instr = sorted(list(uniques))
    size = 500
    window = 5
    model = Word2Vec(sentences, size=size, window=window, workers=4, sg=0, min_count=1)
    vocab = list(model.wv.vocab)
    X = model[vocab]
    labels = vocab
    return X, labels, vocab

# Write clusters to file
def write_clusters(subscript, clusters, vocab):
    f = open("clusters_"+subscript+".txt", 'w')
    for i in range(len(clusters)):
        term = vocab[i]
        clus = str(clusters[i])
        f.write(term + "," + clus + "\n")
    f.close()

# Create cluster plots
def plot_clusters(X, labels, cut_point=0.01):
    #cut_point = 0.1 # Dynamic no library
    #cut_point = 2 # Dynamic
    #cut_point = 0.01 # Static Small
    plt.figure(figsize=(10,7))
    Z = linkage(X, method='ward', metric='euclidean')
    dend = dendrogram(Z, labels=labels)
    plt.axhline(y=cut_point, c='k')
    plt.title('Euclidean Ward Dendrogram of Assembly Commands (Static)')
    clusters = fcluster(Z, cut_point, criterion='distance')
    print(clusters)
    plt.show()
    return clusters

# Load data from files
# <subscript> is the string abbreviation for the pickle object i.e.
# <dir> is the string directory of the files i.e.
def load_files(subscript, dir):
    fl = FileLoader()
    files = os.listdir(dir)
    for f in files:
        if f[-8:] == "only.txt":
            if subsc == "static_small":
                if "search" in f or "sort" in f:
                    fl.addFilename(dir + f)
            else:
                fl.addFilename(dir + f)
    d = fl.getData(type=np.dtype('unicode_'))
    return d

# Primary function to generate clusters
# <subscript> is the string abbreviation for the pickle object i.e.
# <dir> is the string directory of the files i.e. "source/cpp_examples/dynamic_only_no_library/"
def generate_clusters(subscript, dir, pick=True):
    pickle_obj = subscript + ".obj"
    if pick:
        try:
            print("Loading data from pickle")
            fp = open(pickle_obj,'rb')
            d = pickle.load(fp, encoding='unicode_')
        except:
            print("Pickle loading failed")
            print(pickle_obj + " file not found.")
            print("Loading files manually")
            d = load_files(subscript, dir)

            print("Pickling data for faster loading")
            fp = open(pickle_obj,'wb')
            pickle.dump(d, fp)
            fp.close()
            generate_clusters(subscript, pick=True)
    else:
        d = load_files(subscript, dir)

    uniques = set()
    sentences = []
    for data in d:
        uniques.update(data[1])
        sentences.append(list(data[1]))

    X, labels, vocab = word_vec(uniques, sentences)

    clusters = plot_clusters(X, labels)

    write_clusters(subscript, clusters, vocab)

def main():
    subs, dir = "static_small", "source/cpp_examples/assembly/"
    #subs, dir = "static_large", "source/cpp_examples/assembly/"
    #subs, dir = "dynamic", "source/cpp_examples/dynamic_only/"
    #subs, dir = "dynamic_nol", "source/cpp_examples/dynamic_only_no_library/"
    generate_clusters(subs, dir)

main()
