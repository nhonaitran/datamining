import numpy as np
from sklearn.datasets import load_iris
from sklearn.cross_validation import KFold

def fit_model(features, labels):
    '''Learn a simple threshold model'''
    
    # initialize the best accuracy to the worst possible value
    best_acc = -1.0;
    
    # loop over all the features
    for fi in range(features.shape[1]):
        # test every possible threshold value for feature fi
        thresholds = features[:, fi].copy()
        thresholds.sort()
        
        for t in thresholds:
            # determine predictions using t as a threshold
            predictions = (features[:, fi] > t)
            
            # accuracy is the fraction of predictions that match the provided labels
            acc = (predictions == labels).mean()
            
            # test whether reversing the test achieves a better threshold
            rev_acc = (predictions == ~labels).mean()            
            if rev_acc > acc:
                acc = rev_acc
                reverse = True
            else:
                reverse = False
            
            # if this is better the previous best, then swap previous with current best
            if acc > best_acc:
                best_acc = acc
                best_feature = fi
                best_threshold = t
                best_reverse = reverse
    
    return best_threshold, best_feature, best_reverse

def predict(model, features):
    '''Apply a learned model'''    
    threshold, feature, reverse = model
    if reverse:
        return features[:, feature] <= threshold
    else:
        return features[:, feature] > threshold
    
def accuracy(features, labels, model):
    '''Compute the accuracy of the model'''
    predictions = predict(model, features)
    return np.mean(predictions == labels)

data = load_iris()
features = data.data
labels = data.target_names[data.target]

species = ['setosa', 'versicolor', 'virginica']
folds = 10
kf = KFold(features.shape[0], n_folds=folds, shuffle=True)
print('{0:10s} {1:5s} {2:^5s} {3:^30s} {4:^12s} {5:^12s}'.format(
            'species',
            'fold#', 
            'theshold',
            'feature',
            'training acc',
            'testing acc'
        ))
for iris in species:
    i = 1
    for training, testing in kf:
        cur_labels = (labels == iris)
        model = fit_model(features[training], cur_labels[training])
        best_acc_training = accuracy(features[training], cur_labels[training], model)
        best_acc_testing = accuracy(features[testing], cur_labels[testing], model)
        
        
        best_t, best_fi, best_rev = model
        print('{0:10s} {1:5d} {2:8} {3:^20s} (index {4:d}) {5:12.1%} {6:12.1%}'.format(
            iris,
            i, 
            best_t,
            data.feature_names[best_fi],
            best_fi,
            best_acc_training,
            best_acc_testing
        ))
        
        i = i+1
        
    print()
