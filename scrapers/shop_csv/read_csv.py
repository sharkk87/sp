import csv
import os

basedir = os.path.abspath(os.path.dirname(__file__))

with open(basedir + '/26012019_upravdom.csv') as file:
    reader = csv.reader(file)
    data = [i for i in reader]

print(len(data))
