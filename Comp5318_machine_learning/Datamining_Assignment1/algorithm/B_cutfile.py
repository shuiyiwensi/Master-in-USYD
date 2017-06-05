#######
#this program cut file in ten part and will easy to cross test
#####################
import pandas as pd
import csv
reader = pd.read_csv('..\\input\\training_data.csv', header=None, iterator=True)
readerlable = pd.read_csv('..\\temp\\train_labels.csv', header=None, iterator=True)
chunkSize = 2010
for i in range(10):
    if i == 9:
        chunkSize = 2014
    I=str(i+1)
    outputtraindata = '..\\temp\\train_data_' +I+'.csv'
    with open(outputtraindata, 'w', newline='') as csvfile:
        g = reader.get_chunk(chunkSize).values
        spamwriter = csv.writer(csvfile, delimiter=',', quotechar='\n', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerows(g)
    outputtrainlables = '..\\temp\\train_lables_' + I + '.csv'
    with open(outputtrainlables, 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',', quotechar='\n', quoting=csv.QUOTE_MINIMAL)
        a = readerlable.get_chunk(chunkSize).values
        spamwriter.writerows(a)





