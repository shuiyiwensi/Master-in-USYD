import csv
import pandas as pd
import numpy as np
def getlablearray(traininglableslocation,numberofarray2):
    readertrain = pd.read_csv(traininglableslocation, header=None, iterator=True)
    chunkSize2 = numberofarray2
    g = readertrain.get_chunk(chunkSize2).values
    numberlist = g[:,0:1]
    return numberlist
with open('..\\temp\\H_test_lables_predict.csv', newline='') as f:
    reader = csv.reader(f)
    table=[]
    for row in reader:
        print(len(row))
        for g in row:
            table.append(g)
print(len(table))
print(table)

Y=getlablearray('..\\input\\test_data.csv',2500)
print(len(Y))
str=[['','']for i in range(len(Y))]
for i in range(len(Y)):
    str[i][0] = Y[i][0]
    str[i][1] = table[i]



trainfilewrite = '..\\output\\predicted_lables.csv'
with open(trainfilewrite, 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',', quotechar='\n', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerows(str)
