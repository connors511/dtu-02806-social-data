# -*- coding: utf-8 -*-
"""
Created on Thu May  7 10:36:14 2015

@author: Dag
"""

import numpy as np
import sys
from sklearn import cross_validation
from sklearn.ensemble import RandomForestClassifier

sys.path.append("C:/Users/Dag/Dropbox/Forårs semester 2015/Social Data analyse og visualisering 02806/reddit project")

from import_data import reddit_info
limit = 50
try:
    X, y_score, attributeNames, total_count= reddit_info(limit)
except:
    print("error at import")
#%%

y_binned = [0] * len(y_score)
for i in range(len(y_score)):
    if y_score[i] < 0:
        y_binned[i] = 0
    elif y_score[i] < 4:
        y_binned[i] = 1
    else:
        y_binned[i] = 2

X_train_bin, X_test_bin, y_train_bin, y_test_bin = cross_validation.train_test_split(X, y_binned, test_size=0.67, random_state=0)

estimators = [50, 100, 150, 250, 300, 350, 400, 450, 500, 550, 600, 650, 700] # Bagging

sweeps = len(estimators)
acc_rand_forest = [0] * sweeps

for i in estimators:
        clfrand = RandomForestClassifier(n_estimators = i, max_features=4, bootstrap=True, oob_score=True)
        clfrand.fit(X_train_bin,y_train_bin)
        acc_rand_forest[estimators.index(i)] = clfrand.score(X_test_bin, y_test_bin)

opti_esti = estimators[acc_rand_forest.index(np.max(acc_rand_forest))]

n_features = [2, 3, 4, 5, 6, 7, 8, 9,10]

sweeps = len(n_features)
acc_rand_forest = [0] * sweeps

for i in n_features:
        clfrand = RandomForestClassifier(n_estimators = opti_esti , max_features=i, bootstrap=True, oob_score=True)
        clfrand.fit(X_train_bin,y_train_bin)
        acc_rand_forest[n_features.index(i)] = clfrand.score(X_test_bin, y_test_bin)

opti_feat = n_features[acc_rand_forest.index(np.max(acc_rand_forest))]

print("Optimal estimators are %i" % (opti_esti))
print("Optimal features are %i" % (opti_feat))
print("Best score of %0.2f" % (max(acc_rand_forest)))


clfrand = RandomForestClassifier(n_estimators = opti_esti, max_features = opti_feat, bootstrap = True, oob_score = True)
clfrand.fit(X_train_bin, y_train_bin)

#%%
import numpy as np
import matplotlib.pyplot as plt


y_predicted = clfrand.predict(X_test_bin)
n_groups = 3

bins_count_predict = [0] * 3
bins_count_real = [0] * 3

for i in range(3):
    bins_count_predict[i] = np.size(y_predicted[np.where(y_predicted == i)],0)
    bins_count_real[i] = len(np.ravel(np.asarray(y_test_bin)[np.where(np.asarray(y_test_bin) == i)]))

fig, ax = plt.subplots()

index = np.arange(n_groups)
bar_width = 0.35

opacity = 0.8

rects1 = plt.bar(index, bins_count_predict, bar_width,
                 alpha=opacity,
                 color='b',
                 label='Predicted')

rects2 = plt.bar(index + bar_width, bins_count_real, bar_width,
                 alpha=opacity,
                 color='r',
                 label='Real')
bins_score_stuff = [" < 0 " , "0 < score > 4 ", " > 4 "]
plt.xlabel('Bins')
plt.ylabel('Count')
plt.title('Scores predicted in bins')
plt.xticks(index + bar_width, [o for o in bins_score_stuff])
plt.legend()