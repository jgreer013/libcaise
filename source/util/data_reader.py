import numpy as np
from .data_file import DataFile as DF

# General class for reading in data from file
class DataReader:
    def __init__(self, data_file=None, dtype=bool):
        self.type = dtype
        self.file = data_file

    def readFile(self, data_file=None, type=bool):
        if data_file != None:
            self.file = data_file

        self.type = type

        try:
            if self.type == np.dtype('unicode_'):
                return np.loadtxt(self.file.getFullName(), dtype=self.type)
            else:
                return np.fromfile(self.file.getFullName(), dtype=self.type)
        except Exception as e:
            print(e)
            return None
