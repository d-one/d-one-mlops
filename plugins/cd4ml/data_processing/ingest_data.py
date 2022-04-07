# Author:      CD4ML Working Group @ D ONE
# Description: This script takes a folder structure containing multiple CSV files  
#              and aggregates it into a single file.
# ================================================================================

import argparse
import pandas as pd
import os
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


def filter_from_date(item, from_date):
    """
    Returns true if the item is after the from_date
    """
    item = item.replace(".csv", "")
    if from_date is not None:
        if pd.to_datetime(item) < pd.to_datetime(from_date):
            return False
    return True


def filter_to_date(item, from_date):
    """
    Returns true if the item is before the to_date
    """
    item = item.replace(".csv", "")
    if from_date is not None:
        if pd.to_datetime(item) > pd.to_datetime(from_date):
            return False
    return True


def filter_is_csv(item):
    """
    Returns true if the item is a csv file
    """
    return item.endswith(".csv")


def _check_keys(dict_, required_keys):
    """checks if a dict contains all expected keys"""
    for key in required_keys:
        if key not in dict_:
            raise ValueError(f'input argument "data_files" is missing required key "{key}"')
        

def get_data(input_folder, from_date=None, to_date=None):
    """
    Get the aggregated dataframe, consisting of all data inside 'input_folder'
    between 'from_date' and 'to_date'
    
    Args:
       input_folder (str): specifying the folder which stores the data
       from_date (Optional[str]): earliest start date to filter data
       to_date (Optional[str]): last date to filter data
    Returns:
       pd.DataFrame: aggregated data frame
    """
    
    list_of_files = []

    logger.info(f"reads csv files from nested folder {input_folder}")

    for (dirpath, dirnames, filenames) in os.walk(input_folder):
        list_of_files += [os.path.join(dirpath, file) for file in filenames]

    logger.info(f"loaded {len(list_of_files)} CSV files")

    # Make relative paths from absolute file paths
    rel_paths = [os.path.relpath(item, input_folder) for item in list_of_files]

    # Filter out non-csv files
    rel_paths = filter(filter_is_csv, rel_paths)

    # Filter out files before from_date
    rel_paths = filter(lambda x: filter_from_date(
        x, from_date), rel_paths)

    # Filter out files after to_date
    rel_paths = filter(lambda x: filter_to_date(x, to_date), rel_paths)

    # Get absolute paths
    abs_paths = [os.path.join(input_folder, item) for item in rel_paths]

    # Concate all files
    dfs = []
    for item in abs_paths:
        dfs.append(pd.read_csv(item))

    return pd.concat(dfs)
    
    
def ingest_data(input_folder, data_files, from_date=None, to_date=None):
    """
    Save the aggregated dataframe, consisting of all data inside 'input_folder'
    between 'from_date' and 'to_date', to the location specified in
    data_files['raw_data_file']
    
    Args:
        input_folder (str): specifying the folder which stores the data
        data_files (dict): including the key 'raw_data_file', specifying the 
          location of the output data
        from_date (Optional[str]): earliest start date to filter data
        to_date (Optional[str]): last date to filter data
    
    Returns:
        pd.DataFrame: aggregated data frame
    """
    
    _check_keys(data_files, ["raw_data_file"])
    output_file = data_files['raw_data_file']
    
    df = get_data(input_folder, from_date, to_date)
        
    if not os.path.exists(os.path.dirname(output_file)):
        os.mkdir(os.path.dirname(output_file))

    df.to_csv(output_file, index=False)

    logger.info(f"Successfully saved csv {output_file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Aggregate data')
    parser.add_argument('--input_folder', type=str, help='Input file')
    parser.add_argument('--data_files', type=dict, 
                        help='dict including key "raw_data_file" where ingested data will be saved')
    parser.add_argument('--from_date', type=str, help='From date')
    parser.add_argument('--to_date', type=str, help='To date')

    args = parser.parse_args()
    ingest_data(args.input_folder, args.data_files,
                from_date=args.from_date, to_date=args.to_date)