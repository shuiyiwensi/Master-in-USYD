###########
#reduce 10 training data part to lower dimentions
##########

import pandas as pd
import numpy as np
import csv
ufile='..\\temp\\trainU.csv'
average=[5.84333333333,3.054,3.75866666667,1.19866666667]
readU = pd.read_csv(ufile,header=None,delimiter=',').values
U= np.float_(readU[:,0:2])

trainfile='..\\data\\iris.csv'
d = pd.read_csv(trainfile, header=None, delimiter=',').values
print('readfinish')
X = np.float_(d[:, :-1])
for j in range(len(X)):
    for k in range(len(X[0])):
        X[j][k]= X[j][k]-average[k]
result=X.dot(U)
trainfilewrite='..\\temp\\test_data_reduce.csv'
with open(trainfilewrite, 'w', newline='') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',', quotechar='\n', quoting=csv.QUOTE_MINIMAL)
    spamwriter.writerows(result)