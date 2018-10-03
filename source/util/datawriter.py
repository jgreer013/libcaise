import numpy
import scipy
import sklearn
import pandas
import matplotlib
import json
import os
import csv

WORKING_PATH = os.getcwd()
filename = "feature_desc.json"
dir = "/home/mindlab013/repos/DyMal/data/uci_dynamic/"
months = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
years = ["2010", "2011", "2012", "2013", "2014"]
first_month = "11"
last_month = "07"

def get_base(d):
    if type(d) != dict and type(d) != list:
        return [d]
    elif type(d) == list:
        return d
    else:
        ret = []
        k = d.keys()
        for key in k:
            ret.extend(get_base(d[key]))

        return ret

def get_features(json_filename):
    j = json.load(open(json_filename))
    features = get_base(j)
    return features

features = get_features(dir + filename)
LEN = len(features)

# Feature 0 is year, 1 is month, 2 is order, 3 is maliciousness
def get_data(dir, year, month):
    try:
        txt_filename = dir + year + "-" + m + ".txt"
        f = open(txt_filename, 'r')
        lines = f.read().splitlines()
        total = [["0" for i in range(LEN+4)] for j in range(len(lines))]
        for line in range(len(lines)):
                l = lines[line]
                split_line = l.split(" ")
                for i in range(len(split_line)):
                    s = split_line[i]
                    if i == 0:
                        total[line][i] = year
                        total[line][i+1] = month
                        total[line][i+2] = line+1
                        total[line][i+3] = s
                    else:
                        if len(s) > 0:
                            k, v = s.split(":")
                            total[line][int(k)+3] = v
        f.close()
        return total
    except FileNotFoundError as fnf_error:
        print(fnf_error)
        return -1


all_features = ["Year", "Month", "Order", "PercentMalicious"]
all_features.extend(features)
all_data = []
total_rows = 0
for y in years:
    for m in months:
        new_data = get_data(dir,y,m)
        if new_data != -1:
            total_rows += len(new_data)
            all_data.extend(new_data)
all = [all_features]
all.extend(all_data)

with open(dir + "all_data.csv","w") as f:
    writer = csv.writer(f)
    writer.writerows(all)
