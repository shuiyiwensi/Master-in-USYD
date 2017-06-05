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
from numpy import *
import numpy as np
import operator



import time
import matplotlib.pyplot as pl
from sklearn.naive_bayes import GaussianNB
from sklearn import svm

def classify(x_train, y_train, x_test,k):
    dataSetSize = x_train.shape[0]


    sqDiffMat = diffMat**2

    for i in range(len(x_train)):
        for j in range(len(x_train[0])):
            if (sqDiffMat[i][j] == 0):
                sqDiffMat[i][j] = 1000

    sqDistances = sqDiffMat.sum(axis=1)
    distances = sqDistances**0.5
    sortedDistIndicies = distances.argsort()
    classCount={}
    for i in range(k):
        voteIlabel = y_train[sortedDistIndicies[i]]
        classCount[voteIlabel] = classCount.get(voteIlabel,0) + 1
    sortedClassCount = sorted(classCount.items(), key=operator.itemgetter(1), reverse=True)
    return sortedClassCount[0][0]


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
clf = LogisticRegression(multi_class='multinomial', solver='newton-cg', C=18)
for trainsetnumber in range(1):
    # cut train data and test dataq
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.01)
    # train by entropy

    answer = classify(x_train,y_train,x_test,7)
    print(answer)
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

