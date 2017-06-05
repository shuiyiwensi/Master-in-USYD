import numpy as np
import matplotlib.pyplot as pl
import pandas as pd
import csv
import random


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
    new_datamatrix
    testdatamatrix