import pandas as pd
import numpy as np
d = pd.read_csv('..\\temp\\result_matrix_of_CDC.csv', header=None, delimiter=',').values
static = np.float_(d[1:31,1:31])
result=0.0
for i in range(30):
    result = result+static[i][i]
print(result)

result=np.zeros([30,4])

for i in range(30):
    a=0
    b=0
    c=0
    d=0
    a=static[i][i]
    b=np.sum(static[i])-a
    c=np.sum(static.T[i])-a
    d=2010.4-b-c-a
    result[i][0]=a
    result[i][1]=b
    result[i][2]=c
    result[i][3]=d
    print(a,b,c,d)

