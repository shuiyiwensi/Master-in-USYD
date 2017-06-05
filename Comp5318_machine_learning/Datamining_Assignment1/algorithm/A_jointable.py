############
#this part is for join training data with lables
#will out put train_labels.csv in temp file
############
import numpy as np
import pandas as pd
import csv
reader = pd.read_csv('..\\input\\training_data.csv', header=None, iterator=True)
readerlable = pd.read_csv('..\\input\\training_labels.csv', header=None, iterator=True)
dic={}
lables = readerlable.get_chunk(20104).values
for lable in lables:
    dic[lable[0]]=lable[1]
print(len(dic))
chunkSize = 100
chunkSize2=104
q=[['' for i in range(2)] for j in range(20104)]

for i in range(200):
    G = reader.get_chunk(chunkSize).values
    for j in range(chunkSize):
        Q=i * chunkSize + j
        q[Q][0] = G[j][0]
        q[Q][1] = dic[G[j][0]]
    print(i)

G = reader.get_chunk(chunkSize2).values
for j in range(chunkSize2):
    Q=20000+j
    q[Q][0] = G[j][0]
    q[Q][1] = dic[G[j][0]]

with open('..\\temp\\train_labels.csv', 'w', newline='') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',', quotechar='\n', quoting=csv.QUOTE_MINIMAL)
    spamwriter.writerows(q)




