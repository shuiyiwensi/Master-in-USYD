import pandas as pd
import csv
import random
import numpy as np
import scipy as sp
from sklearn import tree
from sklearn.metrics import precision_recall_curve
from sklearn.metrics import classification_report
from sklearn.cross_validation import train_test_split
from sklearn.ensemble import RandomForestClassifier

import time
import matplotlib.pyplot as pl
from sklearn.naive_bayes import GaussianNB
from sklearn import svm
start= time.clock()


data = []
labels = []
with open('..\\temp\\test_data_reduce.csv') as ifile:
        for line in ifile:
            tokens = line.strip().split(',')
            data.append([float(tk) for tk in tokens[:]])
with open('..\\data\\iris.csv') as ifile:
    for line in ifile:
        tokens = line.strip().split(',')
        labels.append(tokens[-1])
x = np.array(data)
labels = np.array(labels)
y = np.zeros(labels.shape)
y[labels == 'Iris-setosa'] = 1
y[labels == 'Iris-versicolor'] = 2
y[labels == 'Iris-virginica'] = 3
print(len(x))

resultoutput = 0
result_for_ten = []
clf = RandomForestClassifier()
for trainsetnumber in range(1):
    # cut train data and test dataq
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.01)
    # train by entropy

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
print(classification_report(y_test_result[0], result_for_ten[0], target_names=['1', '2', '3']))
count = 0
for i in range(len(y_test_result[0])):
    if y_test_result[0][i] == result_for_ten[0][i]:
        count = count + 1
print(count * 100 / len(y_test_result[0]), '%')

X1=[]

K1=[]
point=[]
for i in range(100):
    for j in range(100):
        point.append([(j*(9/100)-5),(i*(1.5+2)/100)-2])
point=np.asarray(point)
answer=clf.predict(point)
Y1=['' for i in range(len(answer))]
print(1)
for i in range(len(answer)):
    if answer[i]==1:
        Y1[i] = 'r'
    if answer[i]==2:
        Y1[i] = 'g'
    if answer[i]==3:
        Y1[i] = 'b'
    pl.scatter(point[i][0], point[i][1],color=Y1[i])
Y2=['' for i in range(len(y))]
for i in range(len(y)):
    if y[i]==1:
        Y2[i] = 'm'
    if y[i]==2:
        Y2[i] = 'y'
    if y[i]==3:
        Y2[i] = 'k'
    pl.scatter([x[i][0]], [x[i][1]], color=Y2[i])
pl.scatter([x[34][0]], [x[34][1]], color='c')
pl.scatter([x[37][0]], [x[37][1]], color='c')
pl.show()

