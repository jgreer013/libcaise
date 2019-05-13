from util.file_loader import FileLoader
from pandas import DataFrame
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os
import numpy as np
import seaborn as sns
from gensim.models import Word2Vec
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster
from sklearn.cluster import DBSCAN
import pickle

subsc = "static_small"
pickle_obj = subsc + ".obj"

def main():
    try:
        print("Loading data from pickle")
        #fp = open("data_pickle.obj",'rb')
        fp = open(pickle_obj,'rb')
        d = pickle.load(fp, encoding='unicode_')
    except:
        print("Pickle loading failed")
        print("Loading files manually")
        fl = FileLoader()
        dir = "source/cpp_examples/assembly/"
        files = os.listdir(dir)
        for f in files:
            if f[-8:] == "only.txt":
                if subsc == "static_small":
                    if "search" in f or "sort" in f:
                        fl.addFilename(dir + f)

                else:
                    fl.addFilename(dir + f)

        d = fl.getData(type=np.dtype('unicode_'))
        print("Pickling data for faster loading")
        fp = open(pickle_obj,'wb')
        pickle.dump(d, fp)
        fp.close()
        return
    uniques = set()
    sentences = []
    for data in d:
        uniques.update(data[1])
        sentences.append(list(data[1]))

    instr = sorted(list(uniques))
    size = 500
    window = 5
    model = Word2Vec(sentences, size=size, window=window, workers=4, sg=0, min_count=1)
    vocab = list(model.wv.vocab)
    print(uniques)
    print(vocab)
    X = model[vocab]
    labels = vocab

    #cut_point = 0.1 # Dynamic no library
    #cut_point = 2 # Dynamic
    cut_point = 0.01 # Static Small
    plt.figure(figsize=(10,7))
    Z = linkage(X, method='ward', metric='euclidean')
    dend = dendrogram(Z, labels=labels)
    plt.axhline(y=cut_point, c='k')
    plt.title('Euclidean Ward Dendrogram of Assembly Commands (Static)')
    clusters = fcluster(Z, cut_point, criterion='distance')
    print(clusters)
    plt.show()
    print(len(vocab))
    print(len(clusters))
    print(len(set(clusters)))


    f = open("clusters_"+subsc+".txt", 'w')
    for i in range(len(clusters)):
        term = vocab[i]
        clus = str(clusters[i])
        f.write(term + "," + clus + "\n")
    f.close()




main()
