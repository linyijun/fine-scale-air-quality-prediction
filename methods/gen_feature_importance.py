
import logging

from methods.clustering import get_k_means_label
from methods.learning_utils import random_forest_classifier



def get_important_feature_name(feature_name, importance):
    """
    Get feature names whose importance != 0.0

    :param feature_name: a list of feature names
    :param importance: a list of importance according to the feature names
    :return: a list of important features, sorted important features with its importance as a dict
    """
    feature_dic = dict(zip(feature_name, importance))
    important_feature_dic = {k: v for k, v in feature_dic.items() if v != 0.0}
    sorted_important_feature = [(k, important_feature_dic[k])
                                for k in sorted(important_feature_dic, key=important_feature_dic.get, reverse=True)]
    important_feature_list = list(important_feature_dic.keys())
    return important_feature_list, sorted_important_feature


def get_important_feature_name_with_percent(feature_name, importance, percent=0.1):
    """
    Get top "percent" of feature names based on importance

    :param feature_name: a list of feature names
    :param importance: a list of importance according to the feature names
    :param percent: percentage of the features
    :return: a list of important features, sorted important features with its importance as a dict
    """
    feature_dic = dict(zip(feature_name, importance))
    sorted_feature = [(k, feature_dic[k])
                      for k in sorted(feature_dic, key=feature_dic.get, reverse=True)]
    num_important_feature = int(len(sorted_feature) * percent)
    sorted_important_feature = sorted_feature[:num_important_feature]
    important_feature_list = [k for (k, v) in sorted_important_feature]
    return important_feature_list, sorted_important_feature

