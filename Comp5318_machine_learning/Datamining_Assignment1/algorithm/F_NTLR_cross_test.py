############
#this code was logistic regression in newton method will run pretty slow
###########


import numpy as np
import matplotlib.pyplot as pl
import pandas as pd
import csv
import random
from scipy.optimize import fmin_l_bfgs_b

maxtimesvalue = 500
realmaxtimes = 1800
times = 150
size = 200
moredimen = 0
pickfortest = 500
resettimes = times
accuracynewreate = 1
judgenumber = 0.0
labletonumberdic = {'Photography': 1, 'Media and Video': 22, 'Cards and Casino': 24, 'Lifestyle': 28, 'Tools': 9,
                    'Entertainment': 18, 'Education': 11, 'Finance': 27, 'Personalization': 13, 'Brain and Puzzle': 10,
                    'Health and Fitness': 5, 'Communication': 6, 'Music and Audio': 8, 'Comics': 21,
                    'Arcade and Action': 4,
                    'Travel and Local': 17, 'Shopping': 7, 'Medical': 15, 'Productivity': 19, 'Books and Reference': 20,
                    'Libraries and Demo': 3, 'Sports': 23, 'Racing': 14, 'Casual': 16, 'News and Magazines': 12,
                    'Sports Games': 30, 'Weather': 29, 'Social': 2, 'Transportation': 26, 'Business': 25}



def hx(weight, x):
    z = weight.T
    Z = z.dot(x)
    result = 1.0 / (1 + np.math.exp(-Z))
    return result


def H(weight, dataarray):
    resulth = 0
    coloumnumber = len(dataarray)
    for i in range(coloumnumber):
        temp = hx(weight, dataarray[i])
        temp2 = dataarray[i].dot(dataarray[i].T)
        resulth = resulth + temp * (1 - temp) * temp2
    resultfinal = resulth / coloumnumber
    return resultfinal


def J(weight, dataarray, y):
    coloumnumber = len(dataarray)
    wordnumber = len(dataarray[0])
    resultJ = np.zeros((wordnumber, 1))
    for i in range(coloumnumber):
        temm = np.asarray([dataarray[i]])
        resultJ = resultJ + ((hx(weight, dataarray[i]) - y[i]) * temm).T
    resultfinal = resultJ / coloumnumber
    return resultfinal


def getlucky(num, list):
    choicelist = []
    if (len(list) < num):
        choicelist = list
    else:
        choicelist = list[0:num]
        return choicelist
    listnumber = len(list)
    while listnumber < num:
        numberinlist = False
        choicearraynumber = random.randint(0, choiceamount)
        for q in choicelist:
            if choicearraynumber == q:
                numberinlist = True

        if numberinlist == False:
            choicelist.append(choicearraynumber)
            listnumber = listnumber + 1
    return choicelist


def creatematrixfromlist(a, X):
    X2 = np.zeros([len(a), len(X[0])])
    for i in range(len(a)):
        X2[i] = X[a[i]]

    return X2


def calculat(weight, dataarray, ynew, times):
    j = 0
    for i in range(times):
        Hresult = 1 / H(weight, dataarray)

        Jresult = J(weight, dataarray, ynew)
        weight = weight - Hresult * Jresult

    return weight


def getlablearray(traininglableslocation, numberofarray2):
    readertrain = pd.read_csv(traininglableslocation, header=None, iterator=True)
    chunkSize2 = numberofarray2
    g = readertrain.get_chunk(chunkSize2).values
    numberlist = g[:, 1:2]
    return numberlist


def getlablesdic(traininglableslocation, numberofarray2):
    readertrain = pd.read_csv(traininglableslocation, header=None, iterator=True)
    labletonumberdic = {}
    numberoflable = 1
    chunkSize2 = numberofarray2
    numberlist = []
    g = readertrain.get_chunk(chunkSize2).values
    for G in g:
        y = G[1:2]
        jud = True
        for ele in labletonumberdic:
            if ele == y[0]:
                numberlist.append(labletonumberdic[ele])
                jud = False
        if jud:
            labletonumberdic[y[0]] = numberoflable
            numberlist.append(numberoflable)
            numberoflable = numberoflable + 1
    return labletonumberdic


################################

################################
def getaverage(X, m):
    for i in range(len(X)):
        X[i] = X[i] / m
    return X


def getdistance(X, central):
    distance = 0.0
    for i in range(len(X)):
        distance = distance + (X[i] - central[i]) ** 2
    return distance


def classfy(X, lable):
    diclable = {}
    diclablesum = {}
    lablecentral = {}
    jud = False
    for i in range(len(lable)):

        if len(diclable) == 0:
            diclable[lable[i][0]] = 1
            diclablesum[lable[i][0]] = X[i]
        else:
            for lableindic in diclable:
                if lable[i][0] == lableindic:
                    jud = True
            if jud:
                diclable[lable[i][0]] = diclable[lable[i][0]] + 1
                diclablesum[lable[i][0]] = diclablesum[lable[i][0]] + X[i]
            else:
                diclable[lable[i][0]] = 1
                diclablesum[lable[i][0]] = X[i]
        jud = False
    for lableindic in diclable:
        lablecentral[lableindic] = getaverage(diclablesum[lableindic], diclable[lableindic])

    return lablecentral


def lablebelong(X, lablecentral):
    devidelength = 0
    lable = ''
    for ele in lablecentral:
        temp = 1 / (getdistance(X, lablecentral[ele]) + 0.01)
        if temp > devidelength:
            lable = ele
            devidelength = temp
    return lable


################################
def returnwronglist(wronglist, lucyforest):
    returnlist = []
    for i in wronglist:
        returnlist.append(lucyforest[i])
    return returnlist


################################
def createlablefromlist(a, X):
    lables = []
    for i in range(len(a)):
        lables.append(X[a[i]])
    return lables


################################
def matrixadd(X, k):
    if k == 0:
        return X
    else:
        m = len(X)
        n = len(X[0])
        newn = n + k ** 2
        newX = np.zeros([m, newn])
        for i in range(m):
            for j in range(n):
                newX[i][j] = X[i][j]
        for i in range(m):
            for j in range(k):
                for j2 in range(k):
                    newX[i][n + j * k + j2] = X[i][j] * X[i][j2]
        return newX


################################
def addnormal(X):
    m = len(X)
    n = len(X[0])
    newX = np.ones([m, n + 1])
    for i in range(m):
        for j in range(1, n + 1):
            newX[i][j] = X[i][j - 1]
    return newX


################################

compfinalmatrix = [['' for i in range(31)] for j in range(31)]
for i in range(1, 31):
    for j in range(1, 31):
        compfinalmatrix[i][j] = 0
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
            Y = getlablearray(trainfilelablesread, 2100)
            if combinetime == 0:
                new_labelsmatrix = Y
                combinetime = combinetime + 1
            else:
                new_labelsmatrix = np.vstack([new_labelsmatrix, Y])
        else:
            I = str(i + 1)
            testfiledataread = '..\\temp\\train_data_reduce' + I + '.csv'
            dt = pd.read_csv(testfiledataread, header=None, delimiter=',').values
            testdatamatrix = np.float_(dt[:])
            testfilelablesread = '..\\temp\\train_lables_' + I + '.csv'
            testlablematrix = getlablearray(testfilelablesread, 2100)

    X = new_datamatrix
    X = matrixadd(X, moredimen)
    X = addnormal(X)
    numberofarray = len(X)
    choiceamount = numberofarray - 1
    weightlenth = len(X[0])
    Y = new_labelsmatrix

    emptylist = []
    luckyfortest = getlucky(pickfortest, emptylist)
    X2 = creatematrixfromlist(luckyfortest, X)
    Y3 = createlablefromlist(luckyfortest, Y)

    Weightfinalt = np.zeros([weightlenth, len(labletonumberdic)])

    times2 = 0
    weight = np.zeros((weightlenth, 1))

    listofweight = []
    finifhprecent = 0
    outputsequence = 0
    for ele in labletonumberdic:
        maxtimes = maxtimesvalue
        Ytrain = np.zeros([numberofarray, 1])
        Y2 = np.zeros([len(X2), 1])
        for i in range(numberofarray):
            if Y[i] == ele:
                Ytrain[i] = 1
            else:
                Ytrain[i] = 0
        for i in range(len(X2)):
            if Y3[i] == ele:
                Y2[i] = 1
            else:
                Y2[i] = 0

        loop = True

        wronglist = []
        while loop:
            accuracyold = 0
            lucky = getlucky(size, returnwronglist(wronglist, luckyfortest))
            weight = calculat(weight, creatematrixfromlist(lucky, X), creatematrixfromlist(lucky, Ytrain), times)
            resultX = (X2.dot(weight))
            j = 0
            k = 0
            kkk = 0
            wronglist = []
            for i in range(len(X2)):
                if ((resultX[i] > 0.5) & (Y2[i] == 0)):
                    kkk = kkk + 1
                    wronglist.append(i)
                if ((resultX[i] < 0.5) & (Y2[i] == 1)):
                    wronglist.append(i)
                if (resultX[i] > 0.5) & (Y2[i] == 1):
                    k = k + 1
                if Y2[i] == 1:
                    j = j + 1
            times2 = times2 + times
            Timess = str(times2)
            accuracynew = (k / (j + 0.001)) * (1 - ((kkk - k) / (len(X2) - j)))  # accuracy get bigger it stops run
            output = 'weight_' + Timess + '_' + ele + '_.csv'
            JJ = str(j)
            ##########################################################
            emptylist = []
            luckyfortest = getlucky(pickfortest, emptylist)
            X2 = creatematrixfromlist(luckyfortest, X)
            Y3 = createlablefromlist(luckyfortest, Y)
            for i in range(len(X2)):
                if Y3[i] == ele:
                    Y2[i] = 1
                else:
                    Y2[i] = 0
                    ##########################################################
            if (times2 >= maxtimes) & ((times2 >= realmaxtimes) | ((k / (j + 0.001) > 0.65) & ((k != 0)))):
                ele2 = labletonumberdic[ele]
                outputsequence = outputsequence + 1
                Weightfinalt[:, ele2 - 1:ele2] = weight
                weight = np.zeros((weightlenth, 1))
                times2 = 0
                fiifhnumber = 100 / len(labletonumberdic)
                finifhprecent = finifhprecent + fiifhnumber;
                loop = False

    #############################

    X2 = testdatamatrix
    X2 = matrixadd(X2, moredimen)
    X2 = addnormal(X2)
    Y3 = testlablematrix
    #############################
    lablecentral = classfy(X, Y)
    #############################
    finalresultoflr = X2.dot(Weightfinalt)
    static = 0
    finalresultoflr2 = finalresultoflr
    for i in range(len(finalresultoflr)):
        for j in range(len(finalresultoflr[0])):
            if finalresultoflr2[i][j] > 0.5:
                finalresultoflr2[i][j] = 1
            else:
                finalresultoflr2[i][j] = 0
    knn = 0
    knnright = 0
    resultassry=[]
    for array in range(len(finalresultoflr)):
        maxnumber = judgenumber
        maxnumbervalue = 0
        #############################
        judtimes = 0
        #############################
        for number in range(len(finalresultoflr[array])):
            if finalresultoflr[array][number] > maxnumber:
                maxnumber = finalresultoflr[array][number]
                maxnumbervalue = number
                judtimes = judtimes + 1
        if (judtimes == 0):
            knn = knn + 1
            newlablr = lablebelong(X2[array], lablecentral)
            resultassry.append(newlablr)
            if newlablr == Y3[array]:
                static = static + 1
                knnright = knnright + 1
        else:
            for ele in labletonumberdic:
                if labletonumberdic[ele] == (maxnumbervalue + 1):
                    resultassry.append(ele)
                    if ele == Y3[array]:
                        static = static + 1

    hahahaha = static / len(finalresultoflr)
    print(static)
    print(knn, knnright)
    print(trainfile,'finalresult=', hahahaha)

    comparematrix = np.zeros([30, 30])
    print(resultassry)
    for i in range(len(Y3)):
        k = labletonumberdic[resultassry[i]] - 1
        temp = Y3[i][0]
        k2 = labletonumberdic[temp] - 1
        comparematrix[k2][k] = comparematrix[k2][k] + 1


    for i in range(1, 31):
        for j in range(1, 31):
            compfinalmatrix[i][j] =compfinalmatrix[i][j]+ comparematrix[i - 1][j - 1]

for i in range(1, 31):
    for j in range(1, 31):
        compfinalmatrix[i][j] = compfinalmatrix[i][j] / 10

trainfilewrite = '..\\temp\\average_result_matrix_of_LR.csv'
with open(trainfilewrite, 'w', newline='') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',', quotechar='\n', quoting=csv.QUOTE_MINIMAL)
    spamwriter.writerows(compfinalmatrix)
















