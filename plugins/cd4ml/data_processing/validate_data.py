# Author:      CD4ML Working Group @ D ONE
# Description: Use this script to validate the raw training and test data. It 
#              asserts nullability and data types with a json config file that
#              either already exists or will be created from the training data.
# ================================================================================

import pandas as pd
from collections import defaultdict
import os
import json

import logging

logger = logging.getLogger(__name__)


def _create_json_config(df):
    """ creates the json config from an input data frame"""
    data_config = defaultdict(dict)

    dtypes_ = df.dtypes.to_dict()
    nulls_ = df.isnull().sum().to_dict()

    for col in df.columns:
        data_config[col]['dtype'] = str(dtypes_[col])
        data_config[col]['nullable'] = nulls_[col] > 0

    return data_config


def _assert_consistency(df, data_config):
    """ asserts consistency of data types an nullability of an input df with a json config"""
    dtypes_ = df.dtypes.to_dict()
    nulls_ = df.isnull().sum().to_dict()
    for col in df.columns:
        has_nulls = nulls_[col] > 0
        assert data_config[col]['dtype'] == str(
            dtypes_[col]), f"{col}: {data_config[col]['dtype']} == {str(dtypes_[col])}"
        assert data_config[col]['nullable'] == has_nulls, f"{col}: {data_config[col]['nullable']} == {has_nulls}"


def _check_keys(dict_, required_keys):
    """checks if a dict contains all expected keys"""
    for key in required_keys:
        if key not in dict_:
            raise ValueError(f'input argument "data_files" is missing required key "{key}"')
        

def validate_data(data_files, configs_dir, **kwargs):
    """
    Loads raw training and test data and validates it for data types and nullability with the 
    'data_config.json' in the configs_dir directory. If there is no data_config.json file, 
    this function creates it from the training data.
    
    Args:
        data_files (dict): contains the following keys:
          'raw_train_file': location of the raw training data
          'raw_test_file': location of the raw test data
        configs_dir (str): path to the configs directory

    """
    required_keys = [
        'raw_train_file',
        'raw_test_file',
    ]
    _check_keys(data_files, required_keys)
    
    df_train = pd.read_csv(data_files['raw_train_file'])
    df_test = pd.read_csv(data_files['raw_test_file'])

    json_file = os.path.join(configs_dir, 'data_config.json')
    if os.path.isfile(json_file):
        with open(json_file, 'r') as f:
            data_config = json.loads(f.read())
            logger.info("loaded {} successfully".format(json_file))
    else:
        data_config = _create_json_config(df_train)
        with open(json_file, 'w') as f:
            json.dump(data_config, f, indent=4)
            logger.info("created {} successfully".format(json_file))

    _assert_consistency(df_train, data_config)
    _assert_consistency(df_test, data_config)