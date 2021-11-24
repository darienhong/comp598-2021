import json 
import argparse 
import pandas as pd
import re
from collections import Counter

# get input arguments 
def get_args(): 
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', type=str)
    parser.add_argument('-o', '--output', type=str)

    return parser.parse_args().input, parser.parse_args().output

# get edges a -> b between ponies and filter out the ones we don't want, make all pony names lowercase
def get_relationships(data_dict, episode_list):
    relationships = {}
    regex = re.compile(r'(?:\W|^)others(?:\W|$)|(?:\W|^)ponies(?:\W|$)|(?:\W|^)and(?:\W|$)|(?:\W|^)all(?:\W|$)')
    for episode in episode_list:
        temp = data_dict[episode].copy()
        temp['pony2'] = temp.copy().shift(1)
        temp = temp[['pony2', 'pony']].rename(columns={'pony': 'pony2', 'pony2': 'pony'}).dropna()
        # filter: any containing 'others', 'ponies', 'and' & speaking to oneself
        temp = temp[~temp['pony'].str.lower().str.contains(regex)]
        temp = temp[~temp['pony2'].str.lower().str.contains(regex)]
        temp['pony'] = temp['pony'].str.lower()
        temp['pony2'] = temp['pony2'].str.lower()
        relationships[episode] = temp[temp['pony'] != temp['pony2']]

    return relationships

# get all chars and the top 101 chars
def get_chars(data_dict, episode_list, num_top=101):
    list_all_chars = set()
    for ep in episode_list:
        set_ep_chars = set(data_dict[ep].pony).union(set(data_dict[ep].pony2))
        list_all_chars = list_all_chars.union(set_ep_chars)
    tmp = dict.fromkeys([*list_all_chars], 0)
    for ep in episode_list:
        for row in data_dict[ep].itertuples(index=False):
            tmp[row[0]] += row[2]
            tmp[row[1]] += row[2]

    return [*list_all_chars], [character for (character, count) in Counter(tmp).most_common(num_top)]

# save the results in json format
def save_json(data_dict, episode_list, top_chars, output_file):
    dic_json = {char: dict.fromkeys(top_chars, 0) for char in top_chars}
    for ep in episode_list:
        for row in data_dict[ep].itertuples(index=False):
            dic_json[row[0]][row[1]] += row[2]
            dic_json[row[1]][row[0]] += row[2]
    dic_json = {char: {other_char: val for other_char, val in dic_json[char].items() if val} for char in top_chars}
    
    with open(output_file, 'w') as file:
        json.dump(dic_json, file, indent=4)

def main(): 
    input_file, output_file = get_args() 
    data = pd.read_csv(input_file, usecols=['title', 'pony'], encoding='utf-8')

     # df raw --> df per episode -> df {cols= pony1, pony2} --> df {cols= pony1, pony2, directed weight}
    data_dict = dict(tuple(data.groupby('title')))
    data_dict = {ep: data_dict[ep].drop('title', axis=1) for ep in data_dict}
    episode_list = [*data_dict]
    data_dict = get_relationships(data_dict, episode_list)
    data_dict = {ep: pd.DataFrame({'weight': data_dict[ep].groupby(['pony', 'pony2']).size()}).reset_index() for ep in episode_list}

    # filter out if the ponies that are not in the top 101 characters
    all_chars, top_chars = get_chars(data_dict, episode_list)
    data_dict = {ep: data_dict[ep][data_dict[ep]['pony'].isin(top_chars)] for ep in episode_list}
    data_dict = {ep: data_dict[ep][data_dict[ep]['pony2'].isin(top_chars)] for ep in episode_list}

    save_json(data_dict, episode_list, top_chars, output_file)
    
if __name__ == "__main__": 
    main()