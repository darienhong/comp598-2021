'''
Script to extract columns we want into a tsv
'''

import json 
import argparse
import pandas as pd

# get arguments 
def get_args(): 
    parser = argparse.ArgumentParser() 
    parser.add_argument('-o', '--output', type=str)
    parser.add_argument('json_input_file', type=str)
    parser.add_argument('num_posts', type=int)
    arguments = parser.parse_intermixed_args()

    return arguments.output, arguments.json_input_file, arguments.num_posts

# load json file and get the Name and Title column
def load_json(json_input): 
    with open(json_input) as f:
        lines = f.read().splitlines()

    # load each line into a pandas dataframe
    data_tmp = pd.DataFrame(lines)
    data_tmp.columns = ['json']
    # apply json loads function and normalize to convert into a flat table
    data = pd.json_normalize(data_tmp['json'].apply(json.loads))

    return data[['data.author_fullname', 'data.title']]


def main(): 
    output_file, json_input, num_posts = get_args() 
    data = load_json(json_input)
    data.columns = ['Name', 'title']
    data = data.reindex(columns=['Name', 'title', 'coding'])

    # if numposts > number of lines, return all lines
    if num_posts > len(data): 
        data.to_csv(output_file, sep='\t', index=False)
    else: 
        # sample num_posts number of posts and put it in tsv file
        data.sample(num_posts).to_csv(output_file, sep='\t', index=False)


if __name__ == "__main__": 
    main()
