import json 
import argparse 
import pandas as pd
import numpy as np 
import networkx as nx
from collections import Counter

def get_args(): 
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', type=str)
    parser.add_argument('-o', '--output', type=str)

    return parser.parse_args().input, parser.parse_args().output

# get edges a -> b between ponies and filter out the ones we don't want, make all pony names lowercase
def get_relationships(data):
    edges = data.copy().shift(1) + '|' + data.copy()
    edges = edges.drop(0)
    # filter: any containing 'others', 'ponies', 'and' & speaking to oneself
    edges = edges[~edges['pony'].str.lower().str.contains('others|ponies|and|all')]
    edges[['pony1', 'pony2']] = edges['pony'].str.split('|', 1, expand=True)
    edges = edges[edges['pony1'] != edges['pony2']]
    edges['pony1'] = edges['pony1'].str.lower()
    edges['pony2'] = edges['pony2'].str.lower()

    return edges

# get undirected graph from directed graph
def get_undir_graph(directed_graph):
    undirected_graph = directed_graph.to_undirected()
    for node in directed_graph:
        for nhbr in nx.neighbors(directed_graph, node): # neighbour
            if node in nx.neighbors(directed_graph, nhbr):
                undirected_graph.edges[node, nhbr]['weight'] = directed_graph.edges[node, nhbr]['weight'] + directed_graph.edges[nhbr, node]['weight']

    return undirected_graph

def get_most_frequent_characters(data_edges, top_num_characters):
    # get dictionary with total interactions per character
    counts = {}
    for row in data_edges.itertuples(index=False):
        if row[0] in counts:
            counts[row[0]] += row[2]
        else:
            counts[row[0]] = row[2]
        if row[1] in counts:
            counts[row[1]] += row[2]
        else:
            counts[row[1]] = row[2]
    # get the top <num_characters> of interaction characters and list of all
    top_chars = [character for (character, count) in Counter(counts).most_common(top_num_characters)]
    all_chars = [character for (character, count) in Counter(counts).most_common()]

    return top_chars, all_chars

def save_json(output_file, data_edges, top_chars, all_chars):
    # construct desired json dictionary structure
    dic = dict.fromkeys(all_chars, {})
    for row in data_edges.itertuples(index=False):
        if dic[row[0]] == {}:
            dic[row[0]] = {row[1]: row[2]}
        else:
            dic[row[0]][row[1]] = row[2]
        if dic[row[1]] == {}:
            dic[row[1]] = {row[0]: row[2]}
        else:
            dic[row[1]][row[0]] = row[2]
    # cleanup: remove values of 0, remove those not in top <n>; and write to output
    dic = {p1: {p2: val for p2, val in dic_w0s.items() if val and p2 in top_chars} for p1, dic_w0s in dic.items() if p1 in top_chars}
    
    with open(output_file, 'w') as file:
        json.dump(dic, file, indent=4)

def main(): 
    input_file, output_file = get_args() 
    data = pd.read_csv(input_file, usecols=['pony'], encoding='utf-8')

    # update data = [pony1, pony2]
    data = get_relationships(data)
    data['weight'] = data.groupby(['pony1', 'pony2'])['pony1'].transform('size')
    print(data)
    directed_graph = nx.from_pandas_edgelist(data, 'pony1', 'pony2', edge_attr='weight')
    undirected_graph = get_undir_graph(directed_graph)

    data_edges = nx.convert_matrix.to_pandas_edgelist(undirected_graph)
    top_chars, all_chars = get_most_frequent_characters(data_edges, top_num_characters=101)
    save_json(output_file, data_edges, top_chars, all_chars)


if __name__ == "__main__": 
    main()