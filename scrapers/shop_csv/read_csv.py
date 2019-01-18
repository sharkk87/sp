import csv

with open('29122018_upravdom.csv') as file:
    reader = csv.reader(file)
    data = [i for i in reader]

print(len(data))
