''' 
Script to analyze annotated files 
'''

import json 
import pandas as pd
import argparse

# get input arguments
def get_args(): 
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', type=str, required=True)
    parser.add_argument('-o', '--output', type=str, required=False)
    args = parser.parse_args()

    return args

def main(): 
    args = get_args() 

    # count of each unique value in 'coding' column
    curr_dic = pd.read_csv(args.input, sep='\t', header=0)['coding'].value_counts().to_dict()
    labels = ['course-related', 'food-related', 'residence-related', 'other']
    keys = ['c', 'f', 'r', 'o']

    for i in range(len(keys)): 
        curr_dic[labels[i]] = curr_dic.pop(keys[i], 0)

    # if no output file is specified print to stdout
    if args.output is None: 
        print(curr_dic)
    else: 
        # save to output file
        json.dump(curr_dic, open(args.output, 'w'), indent=4)

if __name__ == "__main__":
    main()


