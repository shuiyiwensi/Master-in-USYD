# -*- coding: utf-8 -*-
import numpy as np
import scipy as sp
from sklearn import tree
from sklearn.metrics import precision_recall_curve
from sklearn.metrics import classification_report
from sklearn.cross_validation import train_test_split


''' 数据读入 '''
data = []
labels = []
with open('..\\data\\1.txt') as ifile:
        for line in ifile:
            tokens = line.strip().split(',')
            data.append([float(tk) for tk in tokens[:-1]])
            labels.append(tokens[-1])
x = np.array(data)
labels = np.array(labels)
y = np.zeros(labels.shape)


''' 标签转换为0/1 '''
y[labels=='Iris-versicolor']=1

''' 拆分训练数据与测试数据 '''
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.2)
print(y_test)
x_train2, x_train, y_train2, y_train = train_test_split(x_train, y_train, test_size = 0.33)
''' 使用信息熵作为划分标准，对决策树进行训练 '''
clf = tree.DecisionTreeClassifier(criterion='entropy',splitter='best',random_state=1)
print(clf)
clf.fit(x_train, y_train)

''' 把决策树结构写入文件 '''
with open("tree.dot", 'w') as f:
    f = tree.export_graphviz(clf, out_file=f)

''' 系数反映每个特征的影响力。越大表示该特征在分类中起到的作用越大 '''
print(clf.feature_importances_)

'''测试结果的打印'''
answer = clf.predict(x_test)
answer2=clf.predict_proba(x_test)[:,1]

#print(x_train)
#print(np.mean( answer == y_train))

'''准确率与召回率'''
precision, recall, thresholds = precision_recall_curve(y_test, answer)
print(classification_report(y_test, answer, target_names = ['0', '1']))
