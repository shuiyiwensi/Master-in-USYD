###################
#centre distance corsstest
####################

import numpy as np
import matplotlib.pyplot as pl
import pandas as pd
import csv
import random
from scipy.optimize import fmin_l_bfgs_b

trainfile=11
maxtimesvalue=10
realmaxtimes=10
times=10
size=20
moredimen=30
pickfortest=20
resettimes=times
accuracynewreate=1
judgenumber=1
traininglable='training_labels.csv'


labletonumberdic={'Photography': 1, 'Media and Video': 22, 'Cards and Casino': 24, 'Lifestyle': 28, 'Tools': 9,
                  'Entertainment': 18, 'Education': 11, 'Finance': 27, 'Personalization': 13, 'Brain and Puzzle': 10,
                  'Health and Fitness': 5, 'Communication': 6, 'Music and Audio': 8, 'Comics': 21, 'Arcade and Action': 4,
                  'Travel and Local': 17, 'Shopping': 7, 'Medical': 15, 'Productivity': 19, 'Books and Reference': 20,
                  'Libraries and Demo': 3, 'Sports': 23, 'Racing': 14, 'Casual': 16, 'News and Magazines': 12,
                  'Sports Games': 30, 'Weather': 29, 'Social': 2, 'Transportation': 26, 'Business': 25}

def getlablearray(traininglableslocation,numberofarray2):
    readertrain = pd.read_csv(traininglableslocation, header=None, iterator=True)
    chunkSize2 = numberofarray2
    g = readertrain.get_chunk(chunkSize2).values
    numberlist = g[:,1:2]
    return numberlist
def getaverage(X,m):
    for i in range(len(X)):
        X[i]=X[i]/m
    return X

def getdistance(X,central):
    distance=0.0
    for i in range(len(X)):
        distance=distance+(X[i]-central[i])**2
    return distance

def classfy(X,lable):
    diclable={}
    diclablesum={}
    lablecentral={}
    jud=False
    for i in range(len(lable)):

        if len(diclable)==0:
            diclable[lable[i][0]] = 1
            diclablesum[lable[i][0]] = X[i]
        else:
            for lableindic in diclable:
                if lable[i][0] == lableindic:
                    jud=True
            if jud:
                diclable[lable[i][0]] = diclable[lable[i][0]] + 1
                diclablesum[lable[i][0]] = diclablesum[lable[i][0]] + X[i]
            else:
                diclable[lable[i][0]] = 1
                diclablesum[lable[i][0]] = X[i]
        jud = False
    for lableindic in diclable:
        lablecentral[lableindic]=getaverage(diclablesum[lableindic],diclable[lableindic])

    return lablecentral

def lablebelong(X,lablecentral):
    devidelength=0
    lable=''
    for ele in lablecentral:
        temp=1/(getdistance(X,lablecentral[ele])+0.01)
        if temp>devidelength:
            lable=ele
            devidelength=temp
    return lable


compfinalmatrix = [['' for i in range(31)] for j in range(31)]
for i in range(1, 31):
    for j in range(1, 31):
        compfinalmatrix[i][j]=0

for i in range(1, 31):
    for ele in labletonumberdic:
        if labletonumberdic[ele] == i:
            compfinalmatrix[0][i] = ele
for i in range(1, 31):
    for ele in labletonumberdic:
        if labletonumberdic[ele] == i:
            compfinalmatrix[i][0] = ele


for trainsetnumber in range(10):
    trainfile = trainsetnumber + 1
    combinetime = 0
    for i in range(10):
        if (i + 1) != trainfile:
            I = str(i + 1)
            trainfiledataread = '..\\temp\\train_data_reduce' + I + '.csv'
            d = pd.read_csv(trainfiledataread, header=None, delimiter=',').values
            trainpart = np.float_(d[:])
            if combinetime == 0:
                new_datamatrix = trainpart
            else:
                new_datamatrix = np.vstack([new_datamatrix, trainpart])

            trainfilelablesread = '..\\temp\\train_lables_' + I + '.csv'
            Y = getlablearray(trainfilelablesread, 2500)
            if combinetime == 0:
                new_labelsmatrix = Y
                combinetime = combinetime + 1
            else:
                new_labelsmatrix = np.vstack([new_labelsmatrix, Y])
        else:
            I = str(i + 1)
            testfiledataread = '..\\temp\\train_data_reduce'+I+'.csv'
            dt = pd.read_csv(testfiledataread, header=None, delimiter=',').values
            testdatamatrix = np.float_(dt[:])
            testfilelablesread = '..\\temp\\train_lables_' + I + '.csv'
            testlablematrix = getlablearray(testfilelablesread, 2500)

    X = new_datamatrix
    Y = new_labelsmatrix
    lablecentral = classfy(X, Y)
    X2 = testdatamatrix
    Y3 = testlablematrix
    print(len(Y3))
    print(len(Y3[0]))
    resultassry = []
    static = 0
    for array in range(len(X2)):
        newlablr = lablebelong(X2[array], lablecentral)
        resultassry.append(newlablr)
        if newlablr == Y3[array][0]:
            static = static + 1
    print(static / len(X2), '%')
    comparematrix = np.zeros([30, 30])
    for i in range(len(Y3)):
        k = labletonumberdic[resultassry[i]] - 1
        temp = Y3[i][0]
        k2 = labletonumberdic[temp] - 1
        comparematrix[k2][k] = comparematrix[k2][k] + 1

    for i in range(1, 31):
        for j in range(1, 31):
            compfinalmatrix[i][j] = compfinalmatrix[i][j] + comparematrix[i - 1][j - 1]

for i in range(1, 31):
    for j in range(1, 31):
        compfinalmatrix[i][j] = compfinalmatrix[i][j] / 10

trainfilewrite = '..\\temp\\result_matrix_of_CDC.csv'
with open(trainfilewrite, 'w', newline='') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',', quotechar='\n', quoting=csv.QUOTE_MINIMAL)
    spamwriter.writerows(compfinalmatrix)
























