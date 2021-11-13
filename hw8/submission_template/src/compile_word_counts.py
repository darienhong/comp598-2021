import argparse 
import json 
import pandas as pd

def get_args(): 
    parser = argparse.ArgumentParser() 
    parser.add_argument('-o', '--output', type=str)
    parser.add_argument('-d', '--dialog', type=str)

    return parser.parse_args().output, parser.parse_args().dialog

def count_words(dialog_file, stopwords, pony): 
    pony_json =  '{}'
    x = json.loads(pony_json)
    data = pd.read_csv(dialog_file, index_col=False)
    df_twilight_sparkle = (data[data['pony'].str.casefold() == pony.casefold()])['dialog'].str.replace('[^\w\s]',' ')
    df_twilight_sparkle = df_twilight_sparkle.str.lower()
    df_twilight_sparkle = df_twilight_sparkle.str.replace('[^a-zA-Z\s]+', '')
  #   print(df_twilight_sparkle)
    new_df = df_twilight_sparkle.str.split(expand=True).stack().value_counts().reset_index()
    new_df.columns = ['word', 'frequency']
    filtered_df = new_df[(~new_df['word'].isin(stopwords)) & (new_df['frequency'] >= 5)]
  

    for index, row in filtered_df.iterrows():
        temp = {row['word']: row['frequency']}
        x.update(temp)
    
  #  print(json.dumps(x))
    return x 
    
    # print(json.dumps(parsed, indent=4))

 #   print(filtered_df)


def load_stop_words(): 
    stopwords = []
    my_file = open('../data/stopwords.txt', 'r')
    lines = my_file.readlines()
    for word in lines: 
        stopwords.append(word.replace("\n", ""))
    return stopwords

def main(): 
    output_json = json.loads('{}')
    
    output_file, dialog_file = get_args()
    pony_list_caps = ["Twilight Sparkle", "Applejack", "Rarity", "Pinkie Pie", "Rainbow Dash", "Fluttershy"]
    pony_list = ["twilight sparkle", "applejack", "rarity", "pinkie pie", "rainbow dash", "fluttershy"]
    stopwords = load_stop_words()
    for json_pony, pony in zip(pony_list, pony_list_caps): 
        j = count_words(dialog_file, stopwords, pony)
        temp_json = {json_pony: j}
        output_json.update(temp_json)

    with open(output_file, 'w') as f: 
        json.dump(output_json, f, indent=4)


if __name__ == "__main__": 
    main()