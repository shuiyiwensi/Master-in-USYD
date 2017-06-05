################
#use g decent method to out put result
##############

import numpy as np
import pandas as pd
import csv
import random

moredimen = 0
judgenumber = 0.0
trainfile=11

labletonumberdic = {'Photography': 1, 'Media and Video': 22, 'Cards and Casino': 24, 'Lifestyle': 28, 'Tools': 9,
                    'Entertainment': 18, 'Education': 11, 'Finance': 27, 'Personalization': 13, 'Brain and Puzzle': 10,
                    'Health and Fitness': 5, 'Communication': 6, 'Music and Audio': 8, 'Comics': 21,
                    'Arcade and Action': 4,
                    'Travel and Local': 17, 'Shopping': 7, 'Medical': 15, 'Productivity': 19, 'Books and Reference': 20,
                    'Libraries and Demo': 3, 'Sports': 23, 'Racing': 14, 'Casual': 16, 'News and Magazines': 12,
                    'Sports Games': 30, 'Weather': 29, 'Social': 2, 'Transportation': 26, 'Business': 25}


def hx(theta, x):
    return float(1.0) / (1 + np.math.e**(-x.dot(theta)))
def log_gradient(theta, x, y):
    first_calc = hx(theta, x) - np.squeeze(y)
    final_calc = first_calc.T.dot(x)
    return final_calc
def cost_func(theta, x, y):
    log_func_v = hx(theta,x)
    y = np.squeeze(y)
    step1 = y * np.log(log_func_v)
    step2 = (1-y) * np.log(1 - log_func_v)
    final = -step1 - step2
    return np.mean(final)
def grad_desc(theta_values, X, y, lr=.001, converge_change=.001):
   # X = (X - np.mean(X, axis=0)) / np.std(X, axis=0)
    cost_iter = []
    cost = cost_func(theta_values, X, y)
    cost_iter.append([0, cost])
    change_cost = 1
    i = 1
    while(change_cost > converge_change):
        old_cost = cost
        theta_values = theta_values - (lr * log_gradient(theta_values, X, y))
        cost = cost_func(theta_values, X, y)
        cost_iter.append([i, cost])
        change_cost = old_cost - cost
        i+=1
    return theta_values, np.array(cost_iter)
def pred_values(theta, X, hard):
    #normalize
    X = (X - np.mean(X, axis=0)) / np.std(X, axis=0)
    pred_prob = hx(theta, X)
    pred_value = np.where(pred_prob >= .5, 1, 0)
    if hard:
        return pred_value
    return pred_prob

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
    for ele in labletonumberdic:
        if labletonumberdic[ele] == i:
            compfinalmatrix[0][i] = ele
for i in range(1, 31):
    for ele in labletonumberdic:
        if labletonumberdic[ele] == i:
            compfinalmatrix[i][0] = ele



combinetime = 0
for i in range(10):
    if (i + 1) != trainfile:
        I = str(i + 1)
        trainfiledataread = '..\\temp\\train_data_reduce' + I + '.csv'
        d = pd.read_csv(trainfiledataread, header=None, delimiter=',').values
        print(I)
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
if trainfile==11:
    testfiledataread = '..\\temp\\test_data_reduce.csv'
    dt = pd.read_csv(testfiledataread, header=None, delimiter=',').values
    testdatamatrix2 = np.float_(dt[:])

X = new_datamatrix
print(len(X))
numberofarray = len(X)
choiceamount = numberofarray - 1
weightlenth = len(X[0])
Y = new_labelsmatrix
print(len(Y))
Weightfinalt = np.zeros([weightlenth, len(labletonumberdic)])
weight = np.zeros((weightlenth, 1))
for ele in labletonumberdic:
    Ytrain = np.zeros([numberofarray, 1])
    for i in range(numberofarray):
        if Y[i] == ele:
            Ytrain[i] = 1
        else:
            Ytrain[i] = 0

    betas = weight.T[0]
    fitted_values, cost_iter = grad_desc(betas, X, Ytrain)
    weight = np.array(fitted_values).reshape(len(fitted_values), 1)
    ele2 = labletonumberdic[ele]
    Weightfinalt[:, ele2 - 1:ele2] = weight
    weight = np.zeros((weightlenth, 1))

X2 = testdatamatrix2
print(len(testdatamatrix2))
finalresultoflr = np.zeros([len(X2), 30])
for unique in range(30):
    fitted = Weightfinalt[:, unique:unique + 1].T[0]
    result = pred_values(fitted, X2, hard=False)
    finalresultoflr[:, unique:unique + 1] = np.array(result).reshape(len(result), 1)

static = 0
resultassry = []
for array in range(len(finalresultoflr)):
    maxnumber = judgenumber
    maxnumbervalue = 0
    for number in range(len(finalresultoflr[array])):
        if finalresultoflr[array][number] > maxnumber:
            maxnumber = finalresultoflr[array][number]
            maxnumbervalue = number

    for ele in labletonumberdic:
        if labletonumberdic[ele] == (maxnumbervalue + 1):
            resultassry.append(ele)

hahahaha = static / len(finalresultoflr)
print('finish')
print(len(X2))
print(resultassry)
print(len(resultassry))
trainfilewrite = '..\\temp\\H_test_lables_predict.csv'
with open(trainfilewrite, 'w', newline='') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',', quotechar='\n', quoting=csv.QUOTE_MINIMAL)
    spamwriter.writerow(resultassry)

















