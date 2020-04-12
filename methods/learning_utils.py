from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import RandomForestRegressor
from sklearn import preprocessing
from sklearn.linear_model import LinearRegression

import numpy as np

class StandardScaler2:
    """
        Standard the whole input data
    """

    def __init__(self, mean, std):
        self.mean = mean
        self.std = std

    def transform(self, data):
        return (data - self.mean) / self.std

    def inverse_transform(self, data):
        return (data * self.std) + self.mean

#
# def standard_scaler(df):
#     scl = preprocessing.StandardScaler().fit(df)
#     return scl.transform(df)


def random_forest_classifier(x, y, n_estimators=100, max_depth=None):
    clf = RandomForestClassifier(n_estimators=n_estimators, max_depth=max_depth,
                                 random_state=1234)
    clf.fit(x, y)
    return clf


def random_forest_regressor(x, y, x_testing, n_estimators=100, max_depth=10):
    regr = RandomForestRegressor(n_estimators=n_estimators, max_depth=max_depth,
                                 random_state=1234)
    regr.fit(x, y)
    return regr


def norm_to_zero_one(x):
    # Cannot handle missing values
    # min_max_scaler = preprocessing.MinMaxScaler(feature_range=(0, 1)).fit(df)
    # min_max_scaler.transform(df)

    scaled_max, scaled_min = 1, 0
    x_std = (x - np.nanmin(x, axis=0)) / (np.nanmax(x, axis=0) - np.nanmin(x, axis=0))
    x_scaled = x_std * (scaled_max - scaled_min) + scaled_min
    return x_scaled


def standard_norm(x):
    mean = np.nanmean(x, axis=0)
    std = np.nanstd(x, axis=0)
    x_norm = np.divide(x - mean, std, out=np.zeros_like(x-mean), where=std != 0.0)
    return x_norm, mean, std


def linear_regression(x, y):
    linreg = LinearRegression()
    return linreg.fit(x, y)
