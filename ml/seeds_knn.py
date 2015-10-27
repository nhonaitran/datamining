import os
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.cross_validation import KFold
from sklearn.cross_validation import cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from utils import CHART_DIR, DATA_DIR, load_dataset

features, labels = load_dataset('seeds.tsv') #had to write custom function to parse the file since it contains float and string data

# initialize a classifier instance
classifier = KNeighborsClassifier(n_neighbors=5, weights='uniform', 
                                 algorithm='auto', 
                                 leaf_size=30, 
                                 p=2, 
                                 metric='minkowski', 
                                 metric_params=None)

# compute 10-fold cross-validation
means = []
k = 1
for k in range(1, 20, 2):
    classifier.n_neighbors = k

    # normalize all features to same scale
    classifier = Pipeline([('norm', StandardScaler()), ('knn', classifier)])
    
    for training, testing in KFold(features.shape[0], n_folds=10, shuffle=True):  #need to shuffle the features first before creating folds since the labels are created in contiguous manner
        classifier.fit(features[training], labels[training])
        predictions = classifier.predict(features[testing])
        current_mean = np.mean(predictions == labels[testing])
        means.append(current_mean)

    print('10-fold cross-validation mean accuracy         = {0:.1%} for k={1:d}'.format(np.mean(means), k))

    crossed = cross_val_score(classifier, X=features, y=labels, scoring=None, cv=10, n_jobs=1)
    print('10-fold cross-validation using cross_val_score = {0:.1%} for k={1:d}'.format(np.mean(crossed), k))

