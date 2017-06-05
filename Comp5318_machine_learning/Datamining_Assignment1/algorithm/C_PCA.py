################
#
#pca is easy process it will out put average of training data to temp file
#####################


import pandas as pd
import numpy as np
import matplotlib.pyplot as pl
import csv
import operator

def pcaprepared(X):
    m=len(X)
    n=len(X[0])
    average=[0 for i in range(n)]
    for i in range(n):
        for j in range(m):
           average[i]=average[i]+ X[j][i]
    for i in range(len(average)):
        average[i] =average[i]/m
    for i in range(n):
        for j in range(m):
            X[j][i]=X[j][i]-(average[i])
    return X,average

trainfile='..\\input\\training_data.csv'

d = pd.read_csv(trainfile,header=None,delimiter=',').values
print('readfinish')
X = np.float_(d[0:,1:])
X,average=pcaprepared(X)
print(len(X))
print(len(X[0]))
print(len(average))
print('~~')
m=len(X)



print('m=',m)

sigma=1/m *np.dot(X.T, X)
U,s,Vt= np.linalg.svd(sigma, full_matrices=False)
print(len(U))
print(len(U[0]))
print(len(s))
S = np.diag(s)
with open('..\\temp\\trainU.csv', 'w', newline='') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',', quotechar='\n', quoting=csv.QUOTE_MINIMAL)
    spamwriter.writerows(U)
with open('..\\temp\\trains.csv', 'w', newline='') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',', quotechar='\n', quoting=csv.QUOTE_MINIMAL)
    spamwriter.writerow(s)
with open('..\\temp\\trainVt.csv', 'w', newline='') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',', quotechar='\n', quoting=csv.QUOTE_MINIMAL)
    spamwriter.writerows(Vt)
with open('..\\temp\\trainAverage.csv', 'w', newline='') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',', quotechar='\n', quoting=csv.QUOTE_MINIMAL)
    spamwriter.writerow(average)

