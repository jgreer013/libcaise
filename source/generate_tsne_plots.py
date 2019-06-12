from util.file_loader import FileLoader
from pandas import DataFrame
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
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
    sizes = [300]
    windows = [3]
    perplexity = [1]
    learning_rate = [100, 200, 500, 1000, 5000, 100000]
    for size in sizes:
        for window in windows:
            for p in perplexity:
                for lr in learning_rate:
                    model = Word2Vec(sentences, size=size, window=window, workers=4, sg=0)
                    vocab = list(model.wv.vocab)
                    X = model[vocab]
                    tsne = TSNE(n_components=2, perplexity=p, n_iter=10000, method='exact', learning_rate=lr, init='pca')
                    X_tsne = tsne.fit_transform(X)

                    df = DataFrame(X_tsne, index=vocab, columns=['x','y'])

                    fig = plt.figure()
                    ax = fig.add_subplot(1,1,1)
                    ax.scatter(df['x'], df['y'])

                    for word, pos in df.iterrows():

                        ax.annotate(s=word, xy=(pos.x, pos.y))

                    title = "Size " + str(size) + ", Window " + str(window) + ", Perplexity " + str(p) + ", Learning Rate " + str(lr)

                    ax.set_title(title)
                    plt.savefig(title + ".png")
                    plt.close()
                    print(tsne.n_iter_)



main()
