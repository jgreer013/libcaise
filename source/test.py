from util.file_loader import FileLoader
from scipy.spatial import distance
from pandas import DataFrame
from matplotlib import pyplot as plt
import os
import numpy as np
import seaborn as sns



def main():
    fl = FileLoader()
    dir = "source/cpp_examples/bin/"
    files = os.listdir("source/cpp_examples/bin/")
    for f in files:
        fl.addFilename(dir + f)

    d = fl.getData()
    min_len = len(d[0][1])
    for i in range(len(d)):
        data = d[i]
        min_len = min(len(data[1]), min_len)

    for i in range(len(d)):
        d[i][1] = d[i][1][:min_len]

    mat = np.zeros((len(files), len(files)))
    for i in range(len(d)):
        a = d[i][1]
        for j in range(len(d)):
            b = d[j][1]
            mat[i][j] = 1 - distance.jaccard(a,b)

    frame = DataFrame(mat, columns = [data[0].getFilename() for data in d], index = [data[0].getFilename() for data in d])
    print(frame)

    plt.figure(figsize=(14,13))
    sns_plot = sns.heatmap(frame, annot=True, fmt=".1f", square=True)
    plt.title("Jaccard Distance Matrix")
    sns_plot.get_figure().savefig("output.png")

main()
