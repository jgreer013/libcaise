import pandas
import os
from matplotlib import pyplot as plt

class DataReader:
    def __init__(self, filename):
        try:
            d = pandas.read_csv(filename)
            self.data = d
        except FileNotFoundError as err:
            print(err)

    def getData(self):
        return self.data

    def getCols(self, col):
        if type(col) == range:
            col = list(col)
        if type(col) == list:
            if type(col[0]) == int:
                return self.data[self.data.columns[col]]
            elif type(col[0]) == str:
                return self.data[col]
        elif type(col) == int:
            return self.data[self.data.columns[col]]
        elif type(col) == str:
            return self.data[col]

    def getHeaders(self):
        return self.data.columns.values.tolist()

dir = "/home/mindlab013/repos/DyMal/data/uci_dynamic/"
fn = "all_data.csv"
dr = DataReader(dir + fn)

c = dr.getCols(["PercentMalicious"])
plt.hist(c)
plt.title("Distribution of classes")
plt.show()
