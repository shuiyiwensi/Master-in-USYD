import pandas as pd
import csv
import random
import numpy as np
import scipy as sp
from sklearn import tree
from sklearn.metrics import precision_recall_curve
from sklearn.metrics import classification_report
from sklearn.cross_validation import train_test_split
import time
start= time.clock()
result_for_ten=[]
resultoutput=0
for trainsetnumber in range(10):
    trainfile = trainsetnumber + 1
    combinetime = 0
    for i in range(10):
        if (i + 1) != trainfile:
            I = str(i + 1)
            trainfiledataread = '..\\temp\\train_data_' + I + '.csv'
            d = pd.read_csv(trainfiledataread, header=None, delimiter=',').values
            trainpart = np.array(d[:])
            if combinetime == 0:
                new_datamatrix = trainpart
                combinetime = combinetime + 1
            else:
                new_datamatrix = np.vstack([new_datamatrix, trainpart])

        else:
            I = str(i + 1)
            testfiledataread = '..\\temp\\train_data_' + I + '.csv'
            dt = pd.read_csv(testfiledataread, header=None, delimiter=',').values
            testdatamatrix = np.array(dt[:])


    data=np.vstack([new_datamatrix, testdatamatrix])
    x = np.array(data[:,:-1])
    labels = np.array(data[:,-1])
    y = np.zeros(labels.shape)


    y[labels == 'Iris-setosa'] = 1
    y[labels == 'Iris-versicolor'] = 2
    y[labels == 'Iris-virginica'] = 3


    #cut train data and test dataq
    leng=int(0.9*len(x))
    x_train=x[:leng]
    x_test=x[leng:]
    y_train=y[:leng]
    y_test=y[leng:]

    #train by entropy
    clf = tree.DecisionTreeClassifier(criterion='entropy')
    clf.fit(x_train, y_train)
    answer = clf.predict(x_test)
    print(classification_report(y_test, answer, target_names=['1', '2', '3']))
    answer = answer[:, np.newaxis].astype(int).T
    y_test = y_test[:, np.newaxis].astype(int).T

    if resultoutput==0:
        result_for_ten=answer
        y_test_result=y_test
        resultoutput=1
    else:
        result_for_ten = np.hstack([result_for_ten, answer])
        y_test_result=np.hstack([y_test_result, y_test])
    #test precision and recall]
print(classification_report(y_test_result[0], result_for_ten[0], target_names=['1', '2','3']))
count=0
for i in range(len(y_test_result[0])):
    if y_test_result[0][i]==result_for_ten[0][i]:
        count=count+1

print('accuracy=',count*100/len(y_test_result[0]),'%')


epapsed=(time.clock()-start)
print('time used',epapsed)
