import json 
import pandas as pd
import argparse

def get_args(): 
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', type=str, required=True)
    parser.add_argument('-o', '--output', type=str, required=False)
    args = parser.parse_args()

    return args

def main(): 
    args = get_args() 

    curr_dic = pd.read_csv(args.input, sep='\t', header=0)['coding'].value_counts().to_dict()
    print(curr_dic)
    labels = ['course-related', 'food-related', 'residence-related', 'other']
    keys = ['c', 'f', 'r', 'o']

    for i in range(len(keys)): 
        curr_dic[labels[i]] = curr_dic.pop(keys[i], 0)

    if args.output is None: 
        print(curr_dic)
    else: 
        json.dump(curr_dic, open(args.output, 'w'), indent=4)

if __name__ == "__main__":
    main()


