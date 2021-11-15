import argparse
import json
import pandas as pd 
from math import log10
from re import sub

# get arguments
def get_args(): 
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--counts', type=str)
    parser.add_argument('-n', '--num_words', type=int)

    return parser.parse_args().counts, parser.parse_args().num_words

# format output into proper json format
def pretty_print_json(output):
    data_json = json.dumps(output, indent=4)
    data_json = sub(r'\[\n {7}', '[', data_json)
    data_json = sub(r'(?<!\]),\n {7}', ',', data_json)
    data_json = sub(r'\n {4}\]', ']', data_json)
    print(data_json)

def main(): 
    word_counts, num_words = get_args()
    pony_list = ['twilight sparkle', 'applejack', 'rarity', 'pinkie pie', 'rainbow dash', 'fluttershy']
    num_ponies = len(pony_list)
    output = {}

    # load the word counts
    with open(word_counts, 'r') as f: 
        tf_all = json.load(f)
    
    # calculate tf-idf for each word for each pony
    for pony in pony_list: 
        list_w_tf = []
        for word in tf_all[pony].keys(): 
            tf_idf = tf_all[pony][word] * log10(num_ponies / len([0 for p in pony_list if word in tf_all[p].keys()]))
            list_w_tf.append((word, tf_idf))

        # sort words by tf-idf value in descending order
        temp = pd.DataFrame(list_w_tf).sort_values(by=[1], ascending=False)
        # get the top num_words number of words by tf-idf
        output[pony] = temp[0].to_list()[0:num_words]

    pretty_print_json(output)
    

if __name__ == "__main__": 
    main() 