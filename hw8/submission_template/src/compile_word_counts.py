import argparse 
import json 
import pandas as pd

# get commandline arguments 
def get_args(): 
    parser = argparse.ArgumentParser() 
    parser.add_argument('-o', '--output', type=str)
    parser.add_argument('-d', '--dialog', type=str)

    return parser.parse_args().output, parser.parse_args().dialog

# save word counts to given output file in json format
def save_json(output_file, word_count): 
    with open(output_file, 'w') as f: 
        json.dump(word_count, f, indent=4)

# get word count for all ponies 
def filter_word_list(data, stopwords): 
    list_diag = data['dialog'].to_list()
    all_words = [word for sublist in list_diag for word in sublist if word not in stopwords and word.isalpha()]
    wordcount = pd.Series(all_words).value_counts()
    wordcount = wordcount[wordcount >= 5]

    return wordcount.index.tolist()

# get word counts
def count_words(dialog_file, word_count, stopwords, pony_list, no_punc): 
    data = pd.read_csv(dialog_file, encoding='utf-8')[['pony', 'dialog']]
    data = data[data['pony'].str.lower().isin(pony_list)]
    data['dialog'] = data['dialog'].str.lower().str.translate(no_punc).str.split()

    word_list = filter_word_list(data, stopwords)
    # get word counts for each pony
    for pony in pony_list: 
        list_d_pony = data[data['pony'].str.lower() == pony]['dialog'].to_list()
        words_p = [word for dialog in list_d_pony for word in dialog if word in word_list and word.isalpha()]
        word_count[pony] = pd.Series(words_p).value_counts().to_dict()

def compute_with_args(dialog_file, output_file, stopwords_file): 
    word_count = {} 
    no_punc = str.maketrans('()[],-.?!:;#&+0123456789<>', ' ' * 26)
    pony_list = ['twilight sparkle', 'applejack', 'rarity', 'pinkie pie', 'rainbow dash', 'fluttershy']
    
    # load stop words 
    with open(stopwords_file, 'r') as file: 
        stopwords = file.read().splitlines()[6:]

    count_words(dialog_file, word_count, stopwords, pony_list, no_punc)
    save_json(output_file, word_count)


def main(): 
    word_count = {}    
    output_file, dialog_file = get_args()
    no_punc = str.maketrans('()[],-.?!:;#&+0123456789<>', ' ' * 26)
    pony_list = ['twilight sparkle', 'applejack', 'rarity', 'pinkie pie', 'rainbow dash', 'fluttershy']
    
    # load stop words 
    with open('../data/stopwords.txt', 'r') as file: 
        stopwords = file.read().splitlines()[6:]

    count_words(dialog_file, word_count, stopwords, pony_list, no_punc)
    save_json(output_file, word_count)



if __name__ == "__main__": 
    main()