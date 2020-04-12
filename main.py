import pickle
import numpy as np
import datetime

import pandas as pd

import data_loader
from methods import clustering
from data_models.epa_model import *
from data_models.geo_feature_buffer_model import *
from data_models.location_model import *
from methods.learning_utils import random_forest_classifier, standard_norm
from utils import *


def main(locations, labels, geo_vector, **kwargs):

    pd.set_option('precision', 5)
    geo_vector = geo_vector[locations]
    geo_arr, _, _ = standard_norm(np.array(geo_vector))

    rf_tree_num = kwargs.get('rf_classifier_tree_num', 300)
    rf_tree_depth = kwargs.get('rf_classifier_tree_depth', 10)
    model = random_forest_classifier(geo_arr.T, labels, rf_tree_num, rf_tree_depth)

    selected_features = {}
    for f, i in zip(list(geo_vector.index), model.feature_importances_):
        selected_features[f] = i

    json.dump(selected_features, open(kwargs['model_file'], 'w'))


if __name__ == '__main__':

    """ decide the best k for each month """
    # year = 2020
    # epa_obj = LosAngelesEPA2020
    # for month in range(4, 5):
    #     month_str = str(month).rjust(2, '0')
    #     next_month_str = str(month % 12 + 1).rjust(2, '0')
    #     next_year = year if month != 12 else year + 1
    #     start_time = f'{year}-{month_str}-01'
    #     end_time = f'{next_year}-{next_month_str}-01'
    #     epa_air_vector = data_loader.load_air_data(epa_obj, start_time, end_time)
    #     clustering.cluster_main(epa_air_vector, task='get_best_k')

    """ decide the best k for a given month """
    # year = 2020
    # epa_obj = LosAngelesEPA2020
    # month = 4
    # month_str = str(month).rjust(2, '0')
    # start_time = f'{year}-{month_str}-01'
    # end_time = f'{year}-{month_str}-13'
    # epa_air_vector = data_loader.load_air_data(epa_obj, start_time, end_time)
    # clustering.cluster_main(epa_air_vector, task='get_best_k')

    """ compute feature importance for each month """
    n_clusters_2018 = {1: 3, 2: 3, 3: 3, 4: 4, 5: 4, 6: 4,
                       7: 5, 8: 4, 9: 6, 10: 6, 11: 6, 12: 6}
    n_clusters_2019 = {1: 3, 2: 3, 3: 5, 4: 4, 5: 4, 6: 4,
                       7: 5, 8: 5, 9: 6, 10: 6, 11: 6, 12: 6}
    n_clusters_2020 = {1: 5, 2: 5, 3: 4, 4: 4}

    epa_obj = LosAngelesEPA2020
    n_clusters = n_clusters_2020
    epa_loc_obj = LosAngelesEPASensorLocations
    epa_geo_obj = LosAngelesEpaGeoFeature
    _, epa_geo_vector = data_loader.load_geo_data(epa_geo_obj, loc_type='station_id', loc_obj=epa_loc_obj)

    # year = 2020
    # for month in range(1, 13):
    #     month_str = str(month).rjust(2, '0')
    #     next_month_str = str(month % 12 + 1).rjust(2, '0')
    #     next_year = year if month != 12 else year + 1
    #     start_time = f'{year}-{month_str}-01'
    #     end_time = f'{next_year}-{next_month_str}-01'
    #     model_file = f'data/models/{year}-{month_str}-01.json'
    #
    #     epa_air_vector = data_loader.load_air_data(epa_obj, start_time, end_time)
    #     labels = clustering.cluster_main(epa_air_vector, n_clusters=n_clusters[month])
    #
    #     main(list(epa_air_vector.columns), labels, epa_geo_vector, model_file=model_file)

    """ compute feature importance a given month """
    year = 2020
    month = 4
    month_str = str(month).rjust(2, '0')
    start_time = f'{year}-{month_str}-01'
    end_time = f'{year}-{month_str}-13'
    model_file = f'data/models/{year}-{month_str}-01.json'

    epa_air_vector = data_loader.load_air_data(epa_obj, start_time, end_time)
    labels = clustering.cluster_main(epa_air_vector, n_clusters=n_clusters[month])
    main(list(epa_air_vector.columns), labels, epa_geo_vector, model_file=model_file)
