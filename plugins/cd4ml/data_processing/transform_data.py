# Author:      CD4ML Working Group @ D ONE
# Description: Use this script to transform raw input data into a feature set (x)
#              and label set (y)
# ================================================================================

import os
import time
import pandas as pd
import logging

logger = logging.getLogger(__name__)

pd.options.mode.chained_assignment = None  # default='warn'

_errors_to_classify = [0, 3, 5, 7, 8]
_min_power = 0.05


def get_transformed_data(df):
    """
    Transform raw data into input features and labels

    Args:
        df (pd.DataFrame): raw input data
    
    Returns:
        Tuple[pd.DataFrame]: transformed data frames (input features and labels)
    """
    df = df[df['power'] > _min_power]

    features = ['wind_speed', 'power', 'nacelle_direction', 'wind_direction',
                'rotor_speed', 'generator_speed', 'temp_environment',
                'temp_hydraulic_oil', 'temp_gear_bearing', 'cosphi',
                'blade_angle_avg', 'hydraulic_pressure']

    x = df[features].fillna(0)
    if 'categories_sk' in df.columns:
        df['categories_sk'] = df['categories_sk'].fillna(
            0).apply(lambda x: int(x))
        df['categories_sk'] = df['categories_sk'].apply(
            lambda x: x if x in _errors_to_classify else 9)
        y = df['categories_sk']
    else:
        y = pd.DataFrame(None)
    return x, y


def _check_keys(dict_, required_keys):
    """checks if a dict contains all expected keys"""
    for key in required_keys:
        if key not in dict_:
            raise ValueError(f'input argument "data_files" is missing required key "{key}"')
    
    
def transform_data(data_files, **kwargs):
    """
    Reads the raw input training and test data from disk and transforms them 
    according to the preprocessing function 'get_transformed_data'. Saves the output
    x_train.csv, y_train.csv, x_test.csv and y_test.csv into the specified locations.

    Args:
        data_files (dict): contains the following keys:
          'raw_train_file': location of the raw training data
          'raw_test_file': location of the raw test data
          'transformed_x_train_file': where to save the transformed training data (input features)
          'transformed_y_train_file': where to save the transformed training data (labels)
          'transformed_x_test_file': where to save the transformed test data (input features)
          'transformed_y_test_file': where to save the transformed test data (labels)
    """
    required_keys = [
        'raw_train_file',
        'raw_test_file',
        'transformed_x_train_file',
        'transformed_y_train_file',
        'transformed_x_test_file',
        'transformed_y_test_file',
    ]
    _check_keys(data_files, required_keys)
    
    df_train = pd.read_csv(data_files['raw_train_file'])
    logger.info(f'loaded {data_files["raw_train_file"]} successfully')

    df_test = pd.read_csv(data_files['raw_test_file'])
    logger.info(f'loaded {data_files["raw_test_file"]} successfully')

    x_train, y_train = get_transformed_data(df_train)

    x_train.to_csv(data_files['transformed_x_train_file'], index=False)
    logger.info('saved {data_files["transformed_x_train_file"]} successfully')
    
    y_train.to_csv(data_files['transformed_y_train_file'], index=False)
    logger.info('saved {data_files["transformed_y_train_file"]} successfully')

    x_test, y_test = get_transformed_data(df_test)

    x_test.to_csv(data_files['transformed_x_test_file'], index=False)
    logger.info('saved {data_files["transformed_x_test_file"]} successfully')

    y_test.to_csv(data_files['transformed_y_test_file'], index=False)
    logger.info('saved {data_files["transformed_y_test_file"]} successfully')