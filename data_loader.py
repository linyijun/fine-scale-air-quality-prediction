import pandas as pd
from sqlalchemy import literal

from data_models.common_db import session
from utils import *


GEO_COLUMN_SET = [GID_COL, GEO_FEATURE_COL, FEATURE_TYPE_COL, BUFFER_SIZE_COL, VALUE_COL]
AIR_COLUMN_SET = [KEY_COL, TIME_COL, VALUE_COL]


def load_geo_data(geo_obj, loc_type=None, loc_obj=None):

    geo = session.query(geo_obj.gid, geo_obj.geo_feature, geo_obj.feature_type, geo_obj.buffer_size, geo_obj.value).all()

    if loc_type == 'station_id' and loc_obj is not None:
        geo += session.query(loc_obj.station_id, literal('location'), literal('lon'), literal(0), loc_obj.lon).all()
        geo += session.query(loc_obj.station_id, literal('location'), literal('lat'), literal(0), loc_obj.lat).all()
    if loc_type == 'gid' and loc_obj is not None:
        geo += session.query(loc_obj.station_id, literal('location'), literal('lon'), literal(0), loc_obj.lon).all()
        geo += session.query(loc_obj.station_id, literal('location'), literal('lat'), literal(0), loc_obj.lat).all()

    geo_df = pd.DataFrame(geo, columns=GEO_COLUMN_SET)
    geo_vector = construct_geo_vector(geo_df)
    return geo_df, geo_vector


def load_air_data(air_obj, start_time, end_time):

    air_data = session.query(air_obj.station_id, air_obj.date_observed, air_obj.concentration).filter(
        air_obj.date_observed >= start_time, air_obj.date_observed < end_time, air_obj.parameter_name == 'PM2.5').all()

    if len(air_data) < 1:
        return None

    """ remove duplicates and negative values """
    air_df = pd.DataFrame(air_data, columns=AIR_COLUMN_SET)
    air_df = air_df.groupby(by=[KEY_COL, TIME_COL], as_index=False).mean()
    air_df = air_df[air_df[VALUE_COL] > 0]

    """ remove the locations with too few observation """
    n_obs = air_df.groupby(KEY_COL).size().reset_index(name='n')
    rm_loc = list(n_obs[n_obs['n'] < int(0.6 * time_diff(start_time, end_time))][KEY_COL])
    air_df = air_df[~air_df[KEY_COL].isin(rm_loc)]

    """ construct timeseries """
    air_time_series = construct_time_series(air_df)
    return air_time_series


def construct_time_series(input_df):
    """
        Construct the timeseries, indexed by time, columned by locations

    """
    locations = list(input_df[KEY_COL].drop_duplicates())
    time_df = input_df[[TIME_COL]].drop_duplicates().set_index(TIME_COL)

    time_series_list = []
    for loc in locations:
        df = input_df[input_df[KEY_COL] == loc].set_index(TIME_COL)
        df = time_df.join(df, how='left')
        df = df.rename(columns={VALUE_COL: loc})
        time_series_list.append(df[loc])
    time_series = pd.concat(time_series_list, axis=1)
    time_series = time_series.dropna()
    return time_series


def construct_geo_vector(input_df):
    """
    Construct the geo feature vector, indexed by distinct geo feature types, columned by locations

    """
    input_df['feature'] = input_df[GEO_FEATURE_COL] + '_' + input_df[FEATURE_TYPE_COL] + '_' \
                                                          + input_df[BUFFER_SIZE_COL].map(str)
    locations = list(input_df[GID_COL].drop_duplicates())
    features_df = input_df[['feature']].drop_duplicates().set_index('feature')

    feature_vector_list = []
    for loc in locations:
        df = input_df[input_df[GID_COL] == loc].set_index('feature')
        df = features_df.join(df, how='left')
        df = df.rename(columns={VALUE_COL: loc})
        feature_vector_list.append(df[loc])
    feature_vector = pd.concat(feature_vector_list, axis=1)
    feature_vector = feature_vector.fillna(0.0)
    return feature_vector
