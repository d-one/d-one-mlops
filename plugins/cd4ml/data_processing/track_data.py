# Author:      CD4ML Working Group @ D ONE
# Description: Use this script to track the current version of the dataset 
#              located at <data_dir/data.csv> using dvc.
# ================================================================================

import os
import subprocess as sp
from datetime import datetime
import argparse

import logging

logger = logging.getLogger(__name__)


def _initialize_dvc(home_dir, data_dir):
    """initialize .dvc stored in 'home_dir' with data in 'data_dir'"""
    logger.info("initializing DVC repository")
    sp.Popen("git init", shell=True).wait()
    sp.Popen("dvc init", shell=True).wait()
    sp.Popen(f"dvc remote add -d dvc_remote \
        {os.path.join(home_dir, 'dvc_remote')}", shell=True).wait()
    sp.Popen("git commit -m 'dvc setup'", shell=True).wait()
    logger.info("DVC setup committed to Git")


def _check_keys(dict_, required_keys):
    """checks if a dict contains all expected keys"""
    for key in required_keys:
        if key not in dict_:
            raise ValueError(f'input argument "data_files" is missing required key "{key}"')


def track_data(home_dir, data_files, **kwargs):
    """
    Track the raw data stored in data_files['raw_data_file'] with .dvc located in the 'home_dir'

    Args:
        home_dir (str): location of the '.dvc' for data tracking
        data_files (dict): including the key 'raw_data_file', specifying the location of the 
          raw data
    """

    _check_keys(data_files, ['raw_data_file'])
    
    os.chdir(home_dir)
    # Check if DVC was already initialized
    if not os.path.exists(os.path.join(home_dir, ".dvc")):
        logger.info("DVC not yet initialized")
        _initialize_dvc(home_dir, data_files['raw_data_file'])
    
    if not os.popen("dvc status").read() == "Data and pipelines are up to date.\n":
        logger.info("Data update detected")
        logger.info(os.popen("dvc status").read())
        
        # Track current version of dataset
        current_time = datetime.now()
        timestamp = current_time.strftime("%Y/%m/%d-%H:%M:%S")
        sp.Popen(f"dvc add {data_files['raw_data_file']}", shell=True).wait()
        sp.Popen(f"git add {data_files['raw_data_file']}.dvc", shell=True)\
            .wait()
        commit_msg = ' '.join(["adding dataset version", timestamp])
        sp.Popen(f"git commit -m '{commit_msg}'", shell=True).wait()
        logger.info(f"Committed new dataset version {timestamp}")
        sp.Popen("dvc push", shell=True).wait()
        logger.info("Pushed data to remote")
    else:
        logger.info("Dataset did not change. Nothing to track.")
    
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Track data')
    parser.add_argument('--home_dir', type=str, help='root dir')
    parser.add_argument('--data_files', type=dict, help='dict including the key "raw_data_file"')

    args = parser.parse_args()
    track_data(args.home_dir, args.data_dir)
    