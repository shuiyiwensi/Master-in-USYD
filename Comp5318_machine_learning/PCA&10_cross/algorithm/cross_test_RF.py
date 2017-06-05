import pandas as pd
import csv
import random
import numpy as np
import scipy as sp
from sklearn import tree
from sklearn.metrics import precision_recall_curve
from sklearn.metrics import classification_report
from sklearn.cross_validation import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn import svm
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
import time
start= time.clock()

data = []
labels = []
with open('..\\data\\iris.csv') as ifile:
        for line in ifile:
            tokens = line.strip().split(',')
            data.append([float(tk) for tk in tokens[:-1]])
            labels.append(tokens[-1])
x = np.array(data)
labels = np.array(labels)
y = np.zeros(labels.shape)
y[labels == 'Iris-setosa'] = 1
y[labels == 'Iris-versicolor'] = 2
y[labels == 'Iris-virginica'] = 3
print(len(x))
for k in range(1,10):
    resultoutput = 0
    result_for_ten = []
    for trainsetnumber in range(200):
        # cut train data and test dataq
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=k/10)
        # train by entropy
        clf = RandomForestClassifier()
        clf.fit(x_train, y_train)
        answer = clf.predict(x_test)
        answer = answer[:, np.newaxis].astype(int).T
        y_test = y_test[:, np.newaxis].astype(int).T
        if resultoutput == 0:
            result_for_ten = answer
            y_test_result = y_test
            resultoutput = 1
        else:
            result_for_ten = np.hstack([result_for_ten, answer])
            y_test_result = np.hstack([y_test_result, y_test])
            # test precision and recall]
   # print(classification_report(y_test_result[0], result_for_ten[0], target_names=['1', '2', '3']))
    count = 0
    for i in range(len(y_test_result[0])):
        if y_test_result[0][i] == result_for_ten[0][i]:
            count = count + 1
    print(count * 100 / len(y_test_result[0]), '%')
epapsed=(time.clock()-start)
print('time used',epapsed)



