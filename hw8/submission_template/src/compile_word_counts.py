import argparse 
import json 
import pandas as pd

def get_args(): 
    parser = argparse.ArgumentParser() 
    parser.add_argument('-o', '--output', type=str)
    parser.add_argument('-d', '--dialog', type=str)

    return parser.parse_args().output, parser.parse_args().dialog

def count_words(dialog_file, stopwords): 
    data = pd.read_csv(dialog_file)
    df_twilight_sparkle = (data[data['pony'].str.casefold() == "Twilight Sparkle".casefold()])['dialog'].str.replace('[^\w\s]',' ')
    new_df = df_twilight_sparkle.str.split(expand=True).stack().value_counts().reset_index()
    new_df.columns = ['word', 'frequency']
    new_df.drop(new_df.index[new_df['word'] in stopwords], inplace=True)
    print(new_df)

def load_stop_words(): 
    stopwords = []
    my_file = open('../data/stopwords.txt', 'r')
    lines = my_file.readlines()
    for word in lines: 
        stopwords.append(word.replace("\n", ""))
    print(stopwords)
    return stopwords

def main(): 
    output_file, dialog_file = get_args()
    pony_list = ['twilight sparkle', 'applejack', 'rarity', 'pinkie pie', 'rainbow dash', 'fluttershy']
    stopwords = load_stop_words()
    count_words(dialog_file, stopwords)

if __name__ == "__main__": 
    main()