from .data_reader import DataReader as bd
from .data_file import DataFile
import os

class FileLoader:
    def __init__(self, use_clust = False):
        self.filenames = []
        self.use_clust = use_clust
        if use_clust:
            self.key, self.clusters = self.loadClusters()

    def getFilenames(self):
        return self.filenames

    def addFilename(self, f):
        self.filenames.append(f)

    def setFiles(self, filenames):
        self.filenames = filenames

    def getFile(self, ind):
        return self.filenames.get(ind)

    def loadClusters(self):
        fn = "clusters.txt"
        k = {}
        c = {}
        with open(fn, 'r') as f:
            for _, line in enumerate(f):
                term, clus = line.strip().split(',')
                k[term] = clus

                if clus not in c:
                    c[clus] = []

                c[clus].append(term)


        return k, c

    def getData(self, type=bool):
        d = []
        b = bd()
        for f in self.filenames:
            base = os.path.basename(f)
            dir = os.path.dirname(f)
            df = DataFile(dir, base)
            data = b.readFile(df, type=type)
            if self.use_clust:
                for i in range(len(data)):
                    data[i] = self.key[data[i]]
            d.append([df, data])

        return d
