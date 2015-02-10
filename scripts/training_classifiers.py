""" Classifier Training Functions

"""

import pandas as pd
import numpy as np
from sklearn.cross_validation import ShuffleSplit


def normalise_z(features):
    """ Standardise features to have zero mean and unit variance
        Input is a feature matrix
    """
    
    mu = np.mean(features, axis=0)
    sigma = np.std(features, axis=0)
    
    return (features - mu) / sigma
    

def normalise_unit_var(features):
    """ Standardise features to have unit variance
        Input is a feature matrix
    """
    
    sigma = np.std(features, axis=0)
    
    return features / sigma
    
    
def normalise_01(features):
    """ Normalise features to unit interval.  Input is a feature matrix"""
    
    minimum = np.min(features, axis=0)
    maximum = np.max(features, axis=0)
    
    return (features - minimum) / (maximum - minimum)


def draw_random_sample(data, train_size, test_size, random_state=None):
    m = len(data)    
    
    cv = ShuffleSplit(m, n_iter=1, train_size=train_size, test_size=test_size,
                      random_state=random_state)

    train, test = next(iter(cv))
    train_set = data.iloc[train]
    test_set = data.iloc[test]
    
    combined = pd.concat([train_set, test_set], keys=['train', 'test'], names=['test'])
    
    return combined

    
    
def balanced_train_test_split(data, features, target, train_size, test_size):
    grouped = data.groupby(data[target])
    train_test = grouped.apply(lambda x: draw_random_sample(x, train_size, test_size))
    train_test = train_test.swaplevel(0, 1)
    
    X_train = train_test.loc["train", features].as_matrix()
    X_test =  train_test.loc["test", features].as_matrix()
    y_train = train_test.loc["train"][target].as_matrix()
    y_test =  train_test.loc['test'][target].as_matrix()
    
    return X_train, X_test, y_train, y_test