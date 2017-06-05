import numpy as np
import pandas as pd
import matplotlib.pyplot as pl
import csv
import operator


d = pd.read_csv('..\\data\\iris.csv',header=None,delimiter=',').values
X=np.array(d)
for i in range(10):
    X1=X[5*i:5+5*i]
    X2=X[50+5*i:55+5*i]
    X3=X[100+5*i:105+5*i]
    g = np.vstack([X1,X2,X3])
    I=str(i+1)
    outputtraindata = '..\\temp\\train_data_' +I+'.csv'
    with open(outputtraindata, 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',', quotechar='\n', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerows(g)
count=0
for i in range(50):
    X1=X[i]
    X2=X[50+i]
    X3=X[100+i]
    if count==0:
        G = np.vstack([X1, X2, X3])
        count=count+1
    else:
        G = np.vstack([G,X1,X2,X3])
outputtraindata = '..\\temp\\train_data_150.csv'
with open(outputtraindata, 'w', newline='') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',', quotechar='\n', quoting=csv.QUOTE_MINIMAL)
    spamwriter.writerows(G)
