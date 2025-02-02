import json 
import argparse 
import pandas as pd
import networkx as nx

# get input arguments
def get_args(): 
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', type=str)
    parser.add_argument('-o', '--output', type=str)

    return parser.parse_args().input, parser.parse_args().output

# compute the status
def compute_stats(stats_json, data): 

    # create graph from dataframe 
    graph = nx.from_pandas_edgelist(data, 'source', 'target', create_using=nx.Graph(), edge_attr='weight')
    list_edge_degree = sorted([*graph.degree()], key=lambda x: x[1], reverse=True)[0:3]
    list_edge_weight = sorted([*graph.degree(weight='weight')], key=lambda x: x[1], reverse=True)[0:3]
    list_betweeness = sorted([*nx.algorithms.centrality.betweenness_centrality(graph).items()], key=lambda x: x[1], reverse=True)[0:3]

    # populate json file
    stats_json['most_connected_by_num'] = [name for name, edges in list_edge_degree]
    stats_json['most_connected_by_weight'] = [name for name, weight in list_edge_weight]
    stats_json['most_central_by_betweenness'] = [name for name, betweeness in list_betweeness]

    return stats_json

# save stats in json file 
def save_json(output_file, stats_json):
    with open(output_file, 'w') as f1: 
        json.dump(stats_json, f1, indent=4)

def main(): 
    interaction_network, output_file = get_args() 
    stats_json = {}
    
    # create dataframe from json
    with open(interaction_network, 'r') as f: 
        data = pd.json_normalize(json.load(f), sep='|').transpose()
        data[1] = data.index
        data.columns = ['weight', 'edge']
        data[['source', 'target']] = data['edge'].str.split('|', expand=True)
        data = data.drop(columns=['edge'])

    stats_json = compute_stats(stats_json, data)
    save_json(output_file, stats_json)

if __name__ == "__main__": 
    main() 
