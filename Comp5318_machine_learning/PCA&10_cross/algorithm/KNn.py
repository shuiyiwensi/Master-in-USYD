
from __future__ import division
from numpy import *
import numpy as np
import operator
import time
import matplotlib.pyplot as pl

def createDataset():
        data = []
        labels = []
        with open('..\\data\\iris.csv') as ifile:
            for line in ifile:
                tokens = line.strip().split(',')
                data.append([float(tk) for tk in tokens[:-1]])
                labels.append(tokens[-1])
        data = np.array(data)
        labels = np.array(labels)
        x =np.array(data)
        y = np.zeros(labels.shape)
        y[labels == 'Iris-setosa'] = 1
        y[labels == 'Iris-versicolor'] = 2
        y[labels == 'Iris-virginica'] = 3
        return data, y

def classify(x_train, y_train, x_test,k):
    dataSetSize = x_train.shape[0]

    diffMat = tile(x_test, (dataSetSize,1)) - x_train

    sqDiffMat = diffMat**2

    for i in range(sqDiffMat.shape[0]):
        for j in range(sqDiffMat.shape[1]):
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

def result(trainx,trainy,testSetMat2,labelsMat,k):
    datingDataMat=trainx
    datingLabels =trainy    #load data setfrom file
    testSetMat = testSetMat2
    y = labelsMat
    testSize = testSetMat.shape[0]
    correctCount = 0.0
    point = []
    for i in range(testSize):
        for j in range(testSize):
            point.append([(j * (9 / testSize) - 5), (i * (1.5 + 2) / testSize) - 2])
    point = np.asarray(point)

    for i in range(testSize):
        result = classify(datingDataMat, datingLabels,testSetMat[i],k)
        rand = random.randint(1, 10)
        if result == 1:
            pl.scatter(point[i,:],point[i*rand,:],color = 'r')
        if result == 2:
            pl.scatter(point[i,:], point[i*rand,:], color='g')
        if result == 3:
            pl.scatter(point[i,:], point[i*rand,:], color='b')
        print(int_(result))
        if (result == y[i]):
            correctCount += 1.0

    correctRate = correctCount / (float)(len(testSetMat))
    print(correctRate)
    end = time.clock()
    print(end-start)
    pl.show()

if __name__=='__main__':
    result(7)