# Author:      CD4ML Working Group @ D ONE
# Description: Use this script to split the raw input data into a train and
#              test split
# ================================================================================

import os
import pandas as pd
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


def _check_keys(dict_, required_keys):
    """checks if a dict contains all expected keys"""
    for key in required_keys:
        if key not in dict_:
            raise ValueError(f'input argument "data_files" is missing required key "{key}"')
        

def get_train_test_split(df, n_days_test):
    """
    Splits the input data frame into a training and test set

    Args:
        df (pd>dataFrame): raw input data
        n_days_test (int): number of days to consider for test split. The n_days_test last 
          days of the input data will be selected for the test split

    Returns:
        Tuple[pd.DataFrame]: raw train and test data splits
    """

    df['date'] = df['measured_at'].apply(lambda x: x[:10])

    min_date_str = df['date'].min()
    max_date = datetime.strptime(df['date'].max(), '%Y-%m-%d')
    test_dates = [datetime.strftime(max_date - timedelta(days=i), '%Y-%m-%d') 
                  for i in range(n_days_test)]
    
    df_train = df[~df['date'].isin(test_dates)].drop('date', axis=1)
    df_test = df[df['date'].isin(test_dates)].drop('date', axis=1)
    
    logger.info(f"trainset goes from {min_date_str} until {min(test_dates)} (not included)")
    logger.info(f"testset goes from {min(test_dates)} until {max(test_dates)}")
    
    return df_train, df_test
    
        
def split_train_test(data_files, n_days_test=10, **kwargs):
    """
    Splits the input data frame into a training and test set and saves them to disk

    Args:
        data_files (dict): contains the following keys:
          'raw_data_file': location of the raw input data
          'raw_train_file': location of the raw output training data
          'raw_test_file': location of the raw output test data
        n_days_test (int): number of days to consider for test split. The n_days_test last 
          days of the input data will be selected for the test split

    Returns:
        Tuple[pd.DataFrame]: raw train and test data splits
    """
    required_keys = [
        'raw_data_file',
        'raw_train_file',
        'raw_test_file',
    ]
    _check_keys(data_files, required_keys)
        
    input_file = data_files['raw_data_file']
    output_train_file = data_files['raw_train_file']
    output_test_file = data_files['raw_test_file']
    
    df = pd.read_csv(input_file)
    logger.info(f"loaded {input_file} successfully")

    df_train, df_test = get_train_test_split(df, n_days_test)
    
    df_train.to_csv(output_train_file, index=False)
    
    df_test.to_csv(output_test_file, index=False)