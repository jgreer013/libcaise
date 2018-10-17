from .binary_data_reader import BDataReader as bd
from .data_file import DataFile
import os

class FileLoader:
    def __init__(self):
        self.filenames = []

    def getFilenames(self):
        return self.filenames

    def addFilename(self, f):
        self.filenames.append(f)

    def setFiles(self, filenames):
        self.filenames = filenames

    def getFile(self, ind):
        return self.filenames.get(ind)

    def getData(self):
        d = []
        b = bd()
        for f in self.filenames:
            try:
                print(os.listdir())
                base = os.path.basename(f)
                dir = os.path.dirname(f)
                df = DataFile(dir, base)
                data = b.readFile(df)
                d.append([df, data])
            except:
                print("Failure in reading file " + f)

        return d
