from datetime import datetime
import json


def time_diff(start_time, end_time):
    start = datetime.strptime(str(start_time), '%Y-%m-%d')
    end = datetime.strptime(str(end_time), '%Y-%m-%d')
    diff = end - start
    return diff.days * 24


MODEL_CONFIG = {
  "geo_feature_percent": 0.01,
  "n_clusters": 4,
  "n_training_data": 30,
  "rf_classifier_tree_num": 500,
  "rf_classifier_tree_depth": 10,
  "rf_regression_tree_num": 100,
  "rf_regression_tree_depth": 10
}


OSM_GEO_FEATURES = [
    'landuse_a',
    'natural',
    'natural_a',
    'places',
    'places_a',
    'pois',
    'pois_a',
    'railways',
    'roads',
    'traffic',
    'traffic_a',
    'transport',
    'transport_a',
    'water_a',
    'waterways'
]

OTHER_FEATURES = [
    'longitude',
    'latitude'
  ]

KEY_COL = 'station_id'
TIME_COL = 'date_observed'
VALUE_COL = 'value'

GID_COL = 'gid'
GEO_FEATURE_COL = 'geo_feature'
FEATURE_TYPE_COL = 'feature_type'
BUFFER_SIZE_COL = 'buffer_size'

LON_COL = 'lon'
LAT_COL = 'lat'
RESIDUAL_COL = 'residual'
PREDICTION_COL = 'prediction'
PREDICTIONS_COL = 'predictions'


def load_config(file_path):
    json_data = open(file_path).read()
    config = json.loads(json_data)
    return config
