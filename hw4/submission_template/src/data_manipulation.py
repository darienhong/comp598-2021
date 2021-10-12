import pandas as pd 
import numpy as np
import json

def data_collection(): 

    # read from csv file, only take necessary columns (created date, closed date, ZIP, status)
    data_raw = pd.read_csv('nyc_311_limit.csv', usecols=[1, 2, 8, 19], header=None, low_memory=False)
    
    # get incidents opened in 2020 
    data_2020 = data_raw[data_raw[1].str.contains('2020')]

    # get incidents that are closed
    data_closed = data_2020[data_2020[19].str.match('Closed')]
    del data_closed[19]

    # drop any rows that have missing data
    data_nan = data_closed.dropna()

     # reformat: convert open and close to datetime datastructures
    pd.set_option('mode.chained_assignment', None)  # supressing warning
    df_nan[1] = pd.to_datetime(df_nan[1], format='%m/%d/%Y %I:%M:%S %p')
    df_nan[2] = pd.to_datetime(df_nan[2], format='%m/%d/%Y %I:%M:%S %p')
    unique_zip = data_closed[2].unique().tolist()
    json.dump(unique_zip, "output.json", indent=4)

if __name__ == "__main__": 
    data_collection()