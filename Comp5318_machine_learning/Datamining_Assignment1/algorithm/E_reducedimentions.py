###########
#reduce 10 training data part to lower dimentions
##########

import pandas as pd
import numpy as np
import csv
chunksize=0
with open('..\\temp\\trains.csv', newline='') as f:
    reader = csv.reader(f)
    for row in reader:
        print(len(row))
        s = 0.0
        for g in row:
            s = s + abs(float(g))
        jud = 0.90 * s
        print(s)
        print(jud)
        k = 0
        while k<jud:
                k = k + abs(float(row[chunksize]))
                chunksize = chunksize + 1;
        print(chunksize)

sfile='..\\temp\\trainAverage.csv'
ufile='..\\temp\\trainU.csv'
average=[]
with open(sfile,newline='') as f:
    reads = csv.reader(f)
    for row in reads:
        for g in row:
            average.append(float(g))
print(len(average))
for i in range(30):
    print(average[i])
readU = pd.read_csv(ufile,header=None,delimiter=',').values
U= np.float_(readU[:,0:chunksize])

#for i in range(10):
#    I=str(i+1)
#    trainfile='..\\temp\\train_data_' + I + '.csv'
#    d = pd.read_csv(trainfile, header=None, delimiter=',').values
#    print('readfinish')
#    X = np.float_(d[:, 1:])
#    for j in range(len(X)):
#        for k in range(len(X[0])):
#            X[j][k]= X[j][k]-average[k]
#    result=X.dot(U)
#    trainfilewrite='..\\temp\\test_data_reduce _'+ I + '.csv'
#    with open(trainfilewrite, 'w', newline='') as csvfile:
#        spamwriter = csv.writer(csvfile, delimiter=',', quotechar='\n', quoting=csv.QUOTE_MINIMAL)
#        spamwriter.writerows(result)

trainfile='..\\input\\test_data.csv'
d = pd.read_csv(trainfile, header=None, delimiter=',').values
print('readfinish')
X = np.float_(d[:, 1:])
for j in range(len(X)):
    for k in range(len(X[0])):
        X[j][k]= X[j][k]-average[k]
result=X.dot(U)
trainfilewrite='..\\temp\\test_data_reduce.csv'
with open(trainfilewrite, 'w', newline='') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',', quotechar='\n', quoting=csv.QUOTE_MINIMAL)
    spamwriter.writerows(result)