''' 
Compute the average title length given a json file of reddit posts
'''

import pandas as pd 
import json 
import sys 

def load_data(file):
    # load json 
    with open(file) as f: 
        lines = f.read().splitlines()

    # load each line into pandas df 
    df_temp = pd.DataFrame(lines)
    df_temp.columns = ['json']

    # apply json loads function and normalize to convert into a flat table 
    df = pd.json_normalize(df_temp['json'].apply(json.loads))

    return df['data.title']

def main(): 
    file = sys.argv[1] 
    df = load_data(file)

    # print the mean post title length
    print(round(df.str.len().mean(), 2))


if __name__ == "__main__": 
    main()