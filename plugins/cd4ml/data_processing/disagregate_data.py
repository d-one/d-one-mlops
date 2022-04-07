# Author:      CD4ML Working Group @ D ONE
# Description: This script takes a csv file and disaggregates it into multiple 
#              files, parttiioned by the date column.
# ================================================================================

import argparse
import pandas as pd
import os
from tqdm import tqdm
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

parser = argparse.ArgumentParser(description='Disaggregate data')
parser.add_argument('--input_file', type=str, help='Input file')
parser.add_argument('--output_folder', type=str, help='Output folder')
parser.add_argument('--date_column', type=str,
                    help='Date column', default='measured_at')
parser.add_argument('--granularity', type=str,
                    help='Granularity', default='day')
parser.add_argument('--from_date', type=str, help='From date')
parser.add_argument('--to_date', type=str, help='To date')


def get_file_path(fn, folder):
    fns = fn.split("-")
    return os.path.join(folder, *fns[:-1], fns[-1]+".csv")


if __name__ == "__main__":
    args = parser.parse_args()
    granularity = args.granularity

    # Read the data
    df = pd.read_csv(args.input_file)

    # Transforms the date column into a datetime object
    df_index_date = pd.to_datetime(df[args.date_column], utc=True)

    # Define the folder structure for hourly resolution
    if granularity == 'hour':
        df_index_col = df_index_date.dt.year.astype(str) + '-' + df_index_date.dt.month.astype(
            str) + '-' + df_index_date.dt.day.astype(str) + df_index_date.dt.hour.astype(str)

    # Define the folder structure for daily resolution
    if granularity == 'day':
        df_index_col = df_index_date.dt.year.astype(
            str) + '-' + df_index_date.dt.month.astype(str) + '-' + df_index_date.dt.day.astype(str)

    # Define the folder structure for monthly resolution
    if granularity == 'month':
        df_index_col = df_index_date.dt.year.astype(
            str) + '-' + df_index_date.dt.month.astype(str)

    # Define the folder structure for yearly resolution
    if granularity == 'year':
        df_index_col = df_index_date.dt.year.astype(str)

    # Filter the dataframe by the from_date
    if args.from_date is not None:
        selector = df_index_date >= pd.to_datetime(args.from_date, utc=True)
        df_index_col = df_index_col[selector]
        df = df[selector]

    # Filter the dataframe by the to_date
    if args.to_date is not None:
        selector = df_index_date <= pd.to_datetime(args.to_date, utc=True)
        df_index_col = df_index_col[selector]
        df = df[selector]

    # Create the pd Series of output filenames
    df_file_name = df_index_col.apply(
        get_file_path, args=(args.output_folder,))

    # Write the dataframe to the output files
    for ff in tqdm(set(df_file_name)):
        Path(os.path.dirname(ff)).mkdir(parents=True, exist_ok=True)
        df[df_file_name == ff].to_csv(ff, index=False)