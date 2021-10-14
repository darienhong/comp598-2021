import pandas as pd 
import numpy as np
import json
from math import isnan
from datetime import datetime

def data_collection(): 

    # read from csv file, only take necessary columns (created date, closed date, ZIP, status)
    data_raw = pd.read_csv('nyc_311_limit.csv', usecols=[1, 2, 8, 19], header=None, low_memory=False)
    
    # get incidents opened in 2020 
    data_2020 = data_raw[data_raw[1].str.contains('2020')]

    # get incidents that are closed
    data_closed = data_2020[data_2020[19].str.match('Closed')]
    del data_closed[19]

    # drop any rows that have missing data
    data_avail = data_closed.dropna()

    # reformat: convert open and close to datetime datastructures
    pd.set_option('mode.chained_assignment', None)  # supressing warning
    data_avail[1] = pd.to_datetime(data_avail[1], format='%m/%d/%Y %I:%M:%S %p')
    data_avail[2] = pd.to_datetime(data_avail[2], format='%m/%d/%Y %I:%M:%S %p')


    # keep data points where close date is after the open data 
    data_clean = data_avail[data_avail[1] <= data_avail[2]]

    # assign column names and reset index (pretty print)
    data_clean.columns = ['Open', 'Closed', 'ZIP']
    data_clean = data_clean.reset_index(drop=True)

    return data_clean

# create month column and calculate response time 
def data_processing(data_clean): 
    # create month column
    data_processed = data_clean
    data_processed['Month'] = data_processed['Closed'].dt.month

    # calculate response time in hours
    data_processed['Duration (h)'] = (data_processed['Closed'] - data_processed['Open']).dt.total_seconds() / 3600 

    # remove open and close columns 
    del data_processed['Open']
    del data_processed['Closed'] 

    return data_processed


# monthly average for each zipcode 
def monthly_data(data_processed): 
    months_list = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    Month = {} 
    for i in range(1, 13):
        # filter month 
        temp = data_processed[data_processed['Month'] == i]
        del temp['Month']

        # group by ZIP code and calculate mean duration 
        Month[months_list[i - 1]] = temp.groupby('ZIP', as_index=False)['Duration (h)'].mean()


    return Month, months_list


# create dictionary for each zipcode with month values 
def zip_data(unique_zips, Month, months_list): 
    zip_info = {} 
    for zipcode in unique_zips: 
        zip_arr = np.array([])
        for month in months_list: 
            curr_zip = Month[month][Month[month]['ZIP'] == str(zipcode)]
            if curr_zip.empty: 
                month_val = 0 
            else: 
                month_val = curr_zip.values[0, 1]
            zip_arr = np.append(zip_arr, month_val)
        zip_info[int(zipcode)] = zip_arr
    return zip_info 

def save_data(unique_zips, zip_info, monthly_avg_all): 
    # change np arrays to list for json compatibility
    new_zip_dict = {k: v.tolist() for k, v in zip_info.items()}

    # reformatting unique_zips for dashboard simplicity
    tuple_zips = [(x, x) for x in unique_zips]

    # export
    with open('processed_data.json', 'w') as f:
        json.dump([tuple_zips, new_zip_dict, monthly_avg_all], f)

def main(): 

    # collect and filter data
    data_clean = data_collection() 

    # get monthly and duration data
    data_processed = data_processing(data_clean)

    # calculate monthly response time for each ZIP (hrs)
    Month, months_list = monthly_data(data_processed)

    # unique zipcodes 
    unique_zips = sorted(data_processed['ZIP'].unique().tolist())

    # monthly average for each zip
    zip_info = zip_data(unique_zips, Month, months_list)

    # monthly averages for all zips
    monthly_avg_all = [Month[x]['Duration (h)'].mean() if not isnan(Month[x]['Duration (h)'].mean()) else 0
                   for x in months_list]

    
    save_data(unique_zips, zip_info, monthly_avg_all)


if __name__ == "__main__": 
    main()