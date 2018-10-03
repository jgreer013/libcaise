import pandas
import os
import numpy as np
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

dir = os.getcwd() + "/data/uci_dynamic/"
fn = "all_data.csv"
dr = DataReader(dir + fn)

c = dr.getCols("PercentMalicious")

plt.subplot(1,2,1)
plt.hist(c.values, bins=10, histtype="step")
plt.title("General Distribution")
plt.xlabel("Maliciousness")
plt.ylabel("Count")

plt.subplot(1,2,2)
plt.hist(c.values, bins=2, histtype="step")
plt.title("Binary Distribution")
plt.xlabel("Maliciousness")
plt.ylabel("Count")
plt.show()
