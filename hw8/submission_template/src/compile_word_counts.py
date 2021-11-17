import argparse
import json
import pandas as pd
import os
import sys
from pathlib import Path

# get commandline arguments
parentdir = Path(__file__).parents[1]
sys.path.append(parentdir)

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--output', type=str)
    parser.add_argument('-d', '--dialog', type=str)

    return parser.parse_args().output, parser.parse_args().dialog


def get_files(file_data, dir_stop, list_p, no_punc):
    # dialog df
    df = pd.read_csv(file_data, encoding='utf-8')[['pony', 'dialog']]
    df = df[df['pony'].str.lower().isin(list_p)]
    df['dialog'] = df['dialog'].str.lower().str.translate(no_punc).str.split()
    # list_stop
    with open(dir_stop) as file_stop:
        list_stop = file_stop.read().splitlines()[6:]

    return df, list_stop

# save word counts to given output file in json format


def save_json(output_file, word_count):
    with open(output_file, 'w') as f:
        json.dump(word_count, f, indent=4)

# get word count for all ponies


def filter_word_list(data, stopwords):
    list_diag = data['dialog'].to_list()
    all_words = [
        word for sublist in list_diag for word in sublist if word not in stopwords and word.isalpha()]
    wordcount = pd.Series(all_words).value_counts()
    wordcount = wordcount[wordcount >= 5]

    return wordcount.index.tolist()

# get word counts


def count_words(data, pony_list, word_list):
    word_count = {}
    # get word counts for each pony
    for pony in pony_list:
        list_d_pony = data[data['pony'].str.lower() ==
                           pony]['dialog'].to_list()
        words_p = [
            word for dialog in list_d_pony for word in dialog if word in word_list and word.isalpha()]
        word_count[pony] = pd.Series(words_p).value_counts().to_dict()

    return word_count


def compute_word_count_dic(dialog_file, stopwords_file):
    no_punc = str.maketrans('()[],-.?!:;#&', ' ' * 13)
    pony_list = ['twilight sparkle', 'applejack', 'rarity','pinkie pie', 'rainbow dash', 'fluttershy']
    data, stopwords = get_files(dialog_file, stopwords_file, pony_list, no_punc)
    list_words = filter_word_list(data, stopwords)
    word_count = count_words(pony_list, list_words, data)

    return word_count

def main():
    output_file, dialog_file = get_args()
    no_punc = str.maketrans('()[],-.?!:;#&+0123456789<>', ' ' * 26)
    pony_list = ['twilight sparkle', 'applejack', 'rarity','pinkie pie', 'rainbow dash', 'fluttershy']
    stopwords_path = os.path.join(parentdir, 'data', 'stopwords.txt')

    # initialize data
    data, stopwords = get_files(dialog_file, stopwords_path, pony_list, no_punc)

    word_list = filter_word_list(data, stopwords)
    word_count = count_words(data, pony_list, word_list)
    save_json(output_file, word_count)


if __name__ == "__main__":
    main()
