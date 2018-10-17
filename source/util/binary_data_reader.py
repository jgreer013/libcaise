import numpy as np
from .data_file import DataFile as DF

class BDataReader:
    def __init__(self, data_file=None, dtype=bool):
        self.type=dtype
        self.file = data_file

    def readFile(self, data_file=None, type=bool):
        if data_file != None:
            self.file = data_file

        self.type = type

        try:
            return np.fromfile(self.file.getFullName(), self.type)
        except IOError as e:
            print(e)
            return None
