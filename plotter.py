# -*- coding: utf-8 -*-
"""
Created on Sat Apr 18 19:00:19 2015

@author: Dag
"""

import numpy as np
import matplotlib.pyplot as plt
import sys

sys.path.append("D:/Dropbox/Forårs semester 2015/Social Data analyse og visualisering 02806/reddit project")
#sys.path.append("C:/Users/Dag/Dropbox/Forårs semester 2015/Social Data analyse og visualisering 02806/reddit project")
#sys.path.append("/Users/stausgaard/Dropbox/Forars semester 2015/Social Data analyse og visualisering 02806/reddit project")
from import_data import reddit_info
from datetime import datetime
limit = 104863
startTime = datetime.now()
X, y_score, attributeNames, total_count, authorName, subredditName= reddit_info(limit)
print("done with import in " + str(datetime.now()-startTime))

#%% Quantile, dist af comment time
N = 6
ind = np.arange(N)
times_day = ["0-4", "4-8","8-12","12-16","16-20","20-24"]
quant_list = [0] * 6
for i in range(len(quant_list)):
    quant_list[i] = len(np.ravel(np.where(X[:,9] == i)))/limit

width = 0.65
opacity = 0.8

plt.bar(range(6), quant_list, width, color="b", alpha=opacity)
plt.title("Number of comment postings throughout the day")
plt.ylabel("Fraction of posts at day times")
plt.xlabel("Time of day")
plt.grid(True)
plt.xticks(ind+width/2., [o for o in times_day])


#%% Quantiale bar plot, post times of week days
N = 7
ind = np.arange(N)
week_day = ["Mon", "Thue","Wed","Thur","Fri","Sat", "Sun"]
quant_list = [0] * 7
for i in range(len(quant_list)):
    quant_list[i] = len(np.ravel(np.where(X[:,10] == i)))/limit

width = 0.65
plt.bar(range(7), quant_list, width, color="b")
plt.title("Number of comment postings throughout the week")
plt.ylabel("Fraction of posts at week days")
plt.xlabel("Week day")
plt.grid(True)
plt.xticks(ind+width/2., [o for o in week_day])

#%% Distributions of upvotes
# Log since very large spread

# count of positive and negative scores
positive_frac = len(np.asarray(y_score)[np.where(np.asarray(y_score) >0)])/ len(y_score)
neutral_frac = len(np.asarray(y_score)[np.where(np.asarray(y_score) ==0)])/ len(y_score)

print("fraction of positive (>0) %0.2f " % positive_frac)
print("fraction of neutral (==0) %0.2f " % neutral_frac)
print("fraction of negative (<0) %0.2f " % (1 - (positive_frac+neutral_frac)))

#%%
plt.hist(np.log(np.ravel(np.asarray(y_score)[np.where(np.asarray(y_score)>=1)])), bins=40)
plt.title("Distribution of log score")
plt.xlabel("log score")
plt.ylabel("dist. log score")

#%%
def standardize(A):
    return (A-np.mean(A))/(np.std(A))

#%%
plt.scatter((y_score), (X[:,3]), color="b")
plt.title("Score, against comment length")
plt.xlabel("Score")
plt.ylabel("Comment length")

#%%
N = 7
ind = np.arange(N)
width = 0
colors = ["b","r","y","m","g","black"]
temp = np.asarray(y_score)
for i in range(6):
    plt.scatter(i, np.mean(temp[np.where(X[:,9]==i)]), color=colors[i])
plt.title("Score, against time of day")
plt.xlabel("time of day")
plt.xticks(ind+width/2., [o for o in times_day])
plt.ylabel("Mean score")

#%% Mean score versus week day
N = 7
ind = np.arange(N)
colors = ["b","r","y","m","g","black",'0.75']
temp = np.asarray(y_score)
for i in range(7):
    plt.scatter(i, np.mean(temp[np.where(X[:,10]==i)]), color=colors[i])
plt.title("Score, against week day")
plt.xlabel("week day")
plt.xticks(ind, [o for o in week_day])
plt.ylabel("Mean score")

#%%
plt.scatter(y_score, X[:,4], color="b")
plt.title("Score versus Sentiment score")
plt.xlabel("Score")
plt.ylabel("Sentiment score")

#%% Author name length versus score
plt.scatter(y_score, X[:,6], color="b")
plt.title("Score versus author name length")
plt.xlabel("Score")
plt.ylabel("Author Name Length")

#%% Model stuff Linear regression  ----------------------------------------------------
from sklearn import linear_model
from sklearn import cross_validation

X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y_score, test_size=0.67, random_state=0)


regr = linear_model.LinearRegression()
regr.fit(X_train, y_train)

ress = regr.predict(X_test) - y_test
np.mean(np.asarray(ress))

#%% Unlinear, chance of high / low
y_binned = [0] * len(y_score)
for i in range(len(y_score)):
    if y_score[i] < 5:
        y_binned[i] = 0
    else:
        y_binned[i] = 1

N = 2
ind = np.arange(N)
bins_score = ["score < 0", " 0 <= score < 4", "score > 4"]
bins_list = [0] * 2
for i in range(len(bins_list)):
   bins_list[i] = len(np.ravel(np.asarray(y_binned)[np.where(np.asarray(y_binned) == i)]))

width = 0.65
plt.bar(range(2), bins_list, width, color="b")
plt.title("Number of comments in each bin")
plt.ylabel("Count")
plt.xlabel("Week day")
plt.grid(True)
plt.xticks(ind+width/2., [o for o in bins_score])

#%% dec tree to bin prediction   -----------------------------------------
X_train_bin, X_test_bin, y_train_bin, y_test_bin = cross_validation.train_test_split(X, y_binned, test_size=0.67, random_state=0)

from sklearn import tree

clf = tree.DecisionTreeClassifier(criterion="gini")
clf = clf.fit(X_train_bin,y_train_bin)

clf.score(X_test_bin, y_test_bin)

from pylab import rcParams
rcParams['figure.figsize'] = 15, 5 # size of figure

sort_index = np.argsort(clf.feature_importances_)[::-1]

N = len(clf.feature_importances_)
ind = np.arange(N)
width = 0.8
#print( "%.2f %% the score for the decision tree" % (clffold.score(X_test, y_test)*100))


plt.xticks(ind+width/2., np.ravel(attributeNames)[sort_index], rotation=90 )

plt.bar(ind, clf.feature_importances_[sort_index])
plt.ylabel("Gini information gain")
plt.xlabel("attributeNames")
plt.title("Information gain for attributes")
plt.show()

#%%
# Random forest classifier  ----------------------------------
from sklearn.ensemble import RandomForestClassifier
def MSE(y_hat, y):
    return np.sqrt(((y_hat - y) ** 2).mean())

X_train_bin, X_test_bin, y_train_bin, y_test_bin = cross_validation.train_test_split(X, y_binned, test_size=0.67, random_state=0)

estimators = [50, 100, 150, 250, 300, 350, 400, 450, 500] # Bagging

sweeps = len(estimators)
acc_rand_forest = [0] * sweeps

for i in estimators:
        clfrand = RandomForestClassifier(n_estimators = i, max_features=4, bootstrap=True, oob_score=True)
        clfrand.fit(X_train_bin,y_train_bin)
        acc_rand_forest[estimators.index(i)] = clfrand.score(X_test_bin, y_test_bin)
        print("Done with %i of %i" % (i, max(estimators)) )

opti_esti = estimators[acc_rand_forest.index(np.max(acc_rand_forest))]

n_features = [2, 3, 4, 5, 6, 7, 8, 9,10]

sweeps = len(n_features)
acc_rand_forest = [0] * sweeps

for i in n_features:
        clfrand = RandomForestClassifier(n_estimators = opti_esti , max_features=i, bootstrap=True, oob_score=True)
        clfrand.fit(X_train_bin,y_train_bin)
        acc_rand_forest[n_features.index(i)] = clfrand.score(X_test_bin, y_test_bin)
        print("done with %i of %i" % (i, max(n_features)))

opti_feat = n_features[acc_rand_forest.index(np.max(acc_rand_forest))]
clfrand_opti = RandomForestClassifier(n_estimators = opti_esti, max_features = opti_feat, bootstrap=True, oob_score = True)
clfrand_opti.fit(X_train_bin, y_train_bin)

scores = cross_validation.cross_val_score(clfrand_opti, X, y_binned, cv=3)

print("Optimal estimators are %i" % (opti_esti))
print("Optimal features are %i" % (opti_feat))
print("Best score of %0.2f" % (clfrand_opti.score(X_test_bin, y_test_bin)))

#%%
plt.scatter(n_features, acc_rand_forest)
plt.title("Nr. of features")
plt.xlabel("features")
plt.ylabel("Mean squared error")
plt.show()

clfrand.score(X_test_bin, y_test_bin)
#%% --------------------------------- Random forest feature importance
from pylab import rcParams
rcParams['figure.figsize'] = 15, 5 # size of figure

sort_index = np.argsort(clf.feature_importances_)[::-1]

N = len(clf.feature_importances_)
ind = np.arange(N)
width = 0.8

plt.xticks(ind+width/2., np.ravel(attributeNames)[sort_index], rotation=90 )

plt.bar(ind, clf.feature_importances_[sort_index])
plt.ylabel("Gini information gain")
plt.xlabel("attributeNames")
plt.title("Information gain for attributes")
plt.show()

#%%
import numpy as np
import matplotlib.pyplot as plt


y_predicted = clfrand.predict(X_test_bin)
n_groups = 2

bins_count_predict = [0] * 2
bins_count_real = [0] * 2

for i in range(2):
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
bins_score_stuff = [" < 4 " , " > 4 "]
plt.xlabel('Bins')
plt.ylabel('Count')
plt.title('Scores predicted in bins')
plt.xticks(index + bar_width, [o for o in bins_score])
plt.legend()

#%%
indexes_bin = np.where(np.asarray(y_binned)==0)
X_bin_low = np.empty([len(np.ravel(indexes_bin)), len(X[1,:])])
np.copyto(X_bin_low, X[indexes_bin,:])
y_score_low = np.asarray(y_score)[indexes_bin]

X_train_low, X_test_low, y_train_low, y_test_low = cross_validation.train_test_split(X_bin_low, y_score_low, test_size=0.67, random_state=0)

regrlow = linear_model.LinearRegression()
regrlow.fit(X_train_low, y_train_low)

y_predictions_low = [ round(elem,0) for elem in list(regrlow.predict(X_test_low))] # rounded predictions

ress_low = regrlow.predict(X_test_low) - y_test_low
np.mean(np.asarray(ress_low))

#%% Classify with linear and decision  ------------------------------------------------
#def Score_pred(X, y):
from sklearn import tree
from sklearn import cross_validation
from sklearn import linear_model

y_binned = [0] * len(y_score)
for i in range(len(y_score)):
    y_binned[i] = [0,1][y_score[i]>10]

X_train, X_test, y_train_bin, y_test_bin = cross_validation.train_test_split(X, y_binned, test_size=0.67, random_state=0)
X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y_score, test_size=0.67, random_state=0)

y_binned_train = [0] * len(y_train)
for i in range(len(y_train)):
    y_binned_train[i] = [0,1][y_train[i]>10]

indexes_bin_train = np.where(np.asarray(y_binned_train)==0)

indexes_bin_test = np.where(np.asarray(y_binned_train)==1)

X_train_bin_low = np.empty([len(np.ravel(indexes_bin_train)), np.size(X_train,1)])
X_test_bin_low = np.empty([len(np.ravel(indexes_bin_test)), np.size(X_test,1)])

np.copyto(X_train_bin_low, X_train[indexes_bin_train,:])
np.copyto(X_test_bin_low, X_test[indexes_bin_test,:])

clf = tree.DecisionTreeClassifier()
clf = clf.fit(X_train, y_train_bin)

regr = linear_model.LinearRegression()
regr = regr.fit(X_train_bin_low, np.asarray(y_train)[indexes_bin_train])

predictions_bin = clf.predict(X_test_bin_low)
clf.score(X_test_bin_low, np.asarray(y_test_bin)[indexes_bin_test])
   # return predictions_bin