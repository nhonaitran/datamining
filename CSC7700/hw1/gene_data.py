import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from numpy import corrcoef, arange
from pylab import pcolor, show, colorbar, xticks, yticks
from sklearn import preprocessing
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC, l1_min_c
from sklearn.grid_search import GridSearchCV
from sklearn.cross_validation import cross_val_score
import collections

def fitWithLogisticRegression(X, y, cv_fold):
    print("Logistic Regression")

    C_range = l1_min_c(X, y, loss='log') * np.logspace(1, 6)
        
    best_acc = 0.0
    best_c = 1.0
    for c in C_range:
        scores = cross_val_score(LogisticRegression(C=c, penalty='l1'), X, y, scoring='accuracy', cv=cv_fold)
        print '{:10.3f} for [C: {:0.5f}]'.format(scores.mean(), c)
        if (scores.mean() > best_acc):
            best_acc = scores.mean()
            best_c = c
    
    print 'Best {:5.3f} for [C: {:0.5f}]'.format(best_acc, best_c)
    return(best_acc, best_c)

def fitWithDecisionTree(X, y, cv_fold):
    print("Decision Tree")
    
    depth_range = np.arange(3, 11, 1)
    min_samples_leaf_range = np.arange(1, 5, 1)

    best_acc = 0.0
    best_depth = 1
    best_min_leaf = 1

    for depth in depth_range:
        for min_leaf in min_samples_leaf_range:
            scores = cross_val_score(DecisionTreeClassifier(max_depth=depth, min_samples_leaf=min_leaf), X, y, scoring='accuracy', cv=cv_fold)
            print '{:10.3f} for [Depth: {:3d}; Minimumn Leaf:{:3d}] '.format(scores.mean(), best_depth, best_min_leaf )
            if (scores.mean() > best_acc):
                best_acc = scores.mean()
                best_depth = depth
                best_min_leaf = min_leaf
                
    print 'Best {:5.3f} for [Depth: {:3d}; Minimumn Leaf:{:3d}] '.format(best_acc, best_depth, best_min_leaf)
    return(best_acc, best_depth, best_min_leaf)

def fitUsingSVM(X, y, k, cv_fold):
    print("Support Vector Machines ")
    
    C_range = l1_min_c(X, y, loss='log') * np.logspace(0, 7)
    
    if (k == 'linear'):
        param_grid = dict(C=C_range)
    elif (k == 'rbf'):
        gamma_range = 10.0 ** np.arange(-5, 4)
        param_grid = dict(gamma=gamma_range, C=C_range)
    else:
        degree_range = np.arange(2, 8)
        param_grid = dict(degree=degree_range, C=C_range)

    # Tune SVM using exhaustive grid search
    grid = GridSearchCV(SVC(kernel=k), param_grid=param_grid, cv=cv_fold)
    grid.fit(X, y)
    
    for params, mean_score, scores in grid.grid_scores_:
        print("%10.3f for %r" % (mean_score, params))
 
    print("Best %5.3f for %r" % (grid.best_score_, grid.best_params_))
    return(grid.best_score_)
  
def plotColumns(X):
    ixp = np.nonzero(y=='tumor')[0] # index of the positive instances
    ixn = np.nonzero(y=='normal')[0] # index of the negative instances
    for i in range(0,len(df)):       
        fig = plt.figure(figsize=(8,8))
        ax = fig.add_subplot(111)  
        ax.scatter(np.arange(0, len(ixp), 1), X[ixp, i], marker='x', color='red', label='tumor')
        ax.scatter(np.arange(0, len(ixn), 1), X[ixn, i], marker='o', color='green', label='normal')
        ax.set_title("{} column mean={:.2f}; std={:.2f} ".format(df.columns.values[i], X[:,i].mean(), X[:,i].std()))
        plt.show()
    
def plotHist(df):
    
    for i in range(0,len(df)-1):
        col_name = df.columns.values[i]
        plt.figure();
        df[col_name].hist() 
        plt.title("Histogram of {}".format(df.columns.values[i]))
        plt.xlabel(df.columns.values[i])
        plt.ylabel('Frequency')

def printPerfs(perf):
    od = collections.OrderedDict(sorted(perf.items()))

    fig = plt.figure()
    ax = fig.add_subplot(111)  
    ax.bar(range(len(od)), od.values(), width=0.5, align='center')
    ax.set_title('Generalization Performance Comparison\n Prostate Cancer Data Set')
    ax.set_ylabel('Classifiers')
    ax.set_xticks(range(len(od)))
    ax.set_xticklabels(od.keys(), rotation=90)
    ax.grid(b='on')
    plt.show()

df = pd.read_pickle('prostate.df')
X = df.iloc[:,:-1]
y = df.iloc[:, -1]

#X = df.values[:, :-1]
#y = df.values[:, -1]

#plotColumns(X)
#df.hist(by=101, figsize=(6, 4))
#plotHist(df)

cv_fold = 10
perf = dict()
accuracy, C = fitWithLogisticRegression(X, y, cv_fold)
perf["LR_BASE"] = accuracy #

accuracy, depth, min_leaf = fitWithDecisionTree(X, y, cv_fold)
perf["DT_BASE"] = accuracy #

perf["SVM_LIN_BASE"] = fitUsingSVM(X, y, 'linear', cv_fold) # 0.921568627451 #
perf["SVM_RBF_BASE"] = 0.509803921569 #fitUsingSVM(X, y, 'rbf', cv_fold)
perf["SVM_POLY_BASE"] = 0.911764705882 #fitUsingSVM(X, y, 'poly', cv_fold)

printPerfs(perf)

maxx = max(perf.values())             #finds the max value
keys = [x for x,y in perf.items() if y ==maxx]
print 'classifier(s): ', keys, 'with highest accuracy:', maxx
# normalize all columns to range -1 and 1.
#X_norm = (X - X.mean()) / (X.max() - X.min())
#X_norm = preprocessing.normalize(X)
#R = corrcoef(X_norm)
#pcolor(R)

#fig = plt.figure(figsize=(20,20))
#ax = fig.add_subplot(111)
#cax = ax.imshow(R, interpolation='nearest')
#fig.colorbar(cax)
#yticks(arange(101), df.columns.values)
#xticks(arange(101), df.columns.values, rotation=90)
#plt.show()

#accuracy, C = fitWithLogisticRegression(X_norm, y, cv_fold)
#perf["LR_NORM"] = accuracy

#accuracy, depth, min_leaf = fitWithDecisionTree(X_norm, y, cv_fold)
#perf["DT_NORM"] = accuracy

#perf["SVM_LIN_NORM"] = fitUsingSVM(X_norm, y, 'linear', cv_fold)
#perf["SVM_RBF_NORM"] = fitUsingSVM(X_norm, y, 'rbf', cv_fold)
#perf["SVM_POLY_NORM"] = fitUsingSVM(X_norm, y, 'poly', cv_fold)

#printPerfs(perf)
