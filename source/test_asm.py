from util.file_loader import FileLoader
from pandas import DataFrame
from matplotlib import pyplot as plt
import os
import numpy as np
import seaborn as sns
from gensim.models import Word2Vec
from sklearn.manifold import TSNE

def main():
    fl = FileLoader()
    dir = "source/cpp_examples/assembly/"
    files = os.listdir("source/cpp_examples/assembly/")
    for f in files:
        if f[-8:] == "only.txt":
            fl.addFilename(dir + f)

    uniques = set()
    d = fl.getData(type=np.dtype('unicode_'))
    sentences = []
    for data in d:
        uniques.update(data[1])
        sentences.append(list(data[1]))

    instr = sorted(list(uniques))
    model = Word2Vec(sentences, window=2, workers=4)
    vocab = list(model.wv.vocab)
    X = model[vocab]
    tsne = TSNE(n_components=2)
    X_tsne = tsne.fit_transform(X)

    df = DataFrame(X_tsne, index=vocab, columns=['x','y'])

    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    ax.scatter(df['x'], df['y'])

    for word, pos in df.iterrows():
        ax.annotate(word, pos)

    plt.show()


main()
