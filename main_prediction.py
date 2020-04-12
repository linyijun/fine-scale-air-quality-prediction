import os

from datetime import timedelta

import json
import pandas as pd
import numpy as np
import pytz

import data_loader
from data_models.common_db import write_mongodb, session

from data_models.epa_model import *
from data_models.geo_feature_buffer_model import *
from data_models.location_model import *
from methods.learning_utils import random_forest_regressor
from utils import *


AIR_COLUMN_SET = [KEY_COL, TIME_COL, VALUE_COL]


def one_time_prediction(time, epa_geo_vector, fishnet_geo_vector, **kwargs):

    air_data = session.query(epa_obj.station_id, epa_obj.date_observed, epa_obj.concentration).filter(
        epa_obj.date_observed == time, epa_obj.parameter_name == 'PM2.5').all()

    if len(air_data) <= 3:
        return None

    air_df = pd.DataFrame(air_data, columns=AIR_COLUMN_SET)
    air_df = air_df.groupby(by=[KEY_COL, TIME_COL], as_index=False).mean()
    air_df = air_df[air_df[VALUE_COL] > 0]

    locations = list(air_df[KEY_COL])
    y_train = np.array(air_df[VALUE_COL])
    x_train = np.array(epa_geo_vector[locations])
    x_test = np.array(fishnet_geo_vector)

    rf_tree_num = kwargs.get('rf_regression_tree_num', 300)
    rf_tree_depth = kwargs.get('rf_regression_tree_depth', 10)
    model = random_forest_regressor(x_train.T, y_train.T, rf_tree_num, rf_tree_depth)

    prediction = model.predict(x_test.T)
    gids = list(fishnet_geo_vector.columns)
    write_res(gids, prediction, time)


def time_to_time_prediction(epa_geo_vector, fishnet_geo_vector, start_time, end_time):

    time_list = pd.date_range(start=start_time, end=end_time, freq='1H')
    time_list = sorted(list(set([tz.localize(x) for x in time_list])))

    for time in time_list:
        one_time_prediction(time, epa_geo_vector, fishnet_geo_vector)


def write_res(gids, prediction, time):

    """ write results to MongoDB """
    output_list = [{'gid': gid, 'pm25': round(prediction[i], 5)} for i, gid in enumerate(gids)]
    document = {'timestamp': time, 'data': output_list}
    write_mongodb(time, document, f'la_fishnet_2020')

    """ write results to json files """
    # output_list = {gid: round(prediction[i], 5) for i, gid in enumerate(gids)}
    # json.dump(output_list, open(f'./data/{str(time)}_res.json', 'w'))


if __name__ == '__main__':

    year = 2020
    epa_obj = LosAngelesEPA2020
    epa_loc_obj = LosAngelesEPASensorLocations
    epa_geo_obj = LosAngelesEpaGeoFeature
    fishnet_loc_obj = LosAngelesFishnet
    fishnet_geo_obj = LosAngelesFishnetGeoFeature

    _, epa_geo_vector = data_loader.load_geo_data(epa_geo_obj, loc_type='station_id', loc_obj=epa_loc_obj)
    _, fishnet_geo_vector = data_loader.load_geo_data(fishnet_geo_obj, loc_obj=fishnet_loc_obj)

    # for month in range(1, 4):
    #     month_str = str(month).rjust(2, '0')
    #     next_month_str = str(month % 12 + 1).rjust(2, '0')
    #     next_year = year if month != 12 else year + 1
    #     start_time = f'{year}-{month_str}-01'
    #     end_time = f'{next_year}-{next_month_str}-01'
    #
    #     model_file = f'data/models/{year}-{month_str}-01.json'
    #     feature_importance = json.load(open(model_file, 'r'))
    #     features = [k for k, v in sorted(feature_importance.items(), key=lambda item: item[1], reverse=True)]
    #     features = features[: int(len(features) * 0.02)]
    #
    #     this_epa_geo_vector = epa_geo_vector.loc[features]
    #     this_fishnet_geo_vector = fishnet_geo_vector.reindex(features)
    #     this_fishnet_geo_vector = this_fishnet_geo_vector.fillna(0.0)
    #
    #     time_to_time_prediction(this_epa_geo_vector, this_fishnet_geo_vector, start_time, end_time)

    """ Current time request, every time query the last hour data """

    tz = pytz.timezone('America/Los_Angeles')
    current_time = tz.localize(datetime.now().replace(minute=0, second=0, microsecond=0, tzinfo=None))
    current_time = current_time - timedelta(hours=1)
    current_month = str(current_time.month).rjust(2, '0')
    model_file = f'data/models/{current_time.year}-{current_month}-01.json'

    if os.path.exists(model_file):
        feature_importance = json.load(open(model_file, 'r'))
    else:
        feature_importance = json.load(open(f'data/models/2020-04-01.json', 'r'))

    features = [k for k, v in sorted(feature_importance.items(), key=lambda item: item[1], reverse=True)]
    features = features[: int(len(features) * 0.02)]

    this_epa_geo_vector = epa_geo_vector.loc[features]
    this_fishnet_geo_vector = fishnet_geo_vector.reindex(features)
    this_fishnet_geo_vector = this_fishnet_geo_vector.fillna(0.0)
    one_time_prediction(current_time, this_epa_geo_vector, this_fishnet_geo_vector)
