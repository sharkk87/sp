import collections, csv

with open('01112018_upravdom.csv') as file:
    reader = csv.reader(file)
    l = [i[1] for i in reader]
    print(len(l))

    
c = collections.Counter()
for word in l:
    # print(word)
    c[word] += 1

for i in c:
    if c[i] == 2:
        print(i)
