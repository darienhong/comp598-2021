import pandas as pd 
import numpy as np
import csv

def data_collection(): 
    data = pd.read_csv('../data/IRAhandle_tweets_1.csv', nrows=10000)
 
    # keep the tweets that are in english 
  
    data_english = data[data['language'] == 'English']
    print(data_english)
    data_question = data_english[~data_english['content'].str.contains("?", regex=False)]
    print(data_question)
    data_question.to_csv('new_data.tsv', sep='\t', index=False)

  
    data_question['trump_mention'] = np.where(data_question['content'].str.contains('\\bTrump\\b'), True, False)
    header = ["tweet_id", "publish_date", "content", "trump_mention"]
    data_question.to_csv('../dataset.tsv', sep='\t', index=False, columns = header)
    frac = len(data_question[data_question['trump_mention'] == True])  / len(data_question)
    print(len(data_question))
    print(frac)
    save_results(frac)


def save_results(frac): 
    with open("../results.tsv", "w") as file: 
        tsv_writer = csv.writer(file, delimiter="\t")
        tsv_writer.writerow(['result', 'value'])
        tsv_writer.writerow(['frac-trump-mentions', '%.3f'%(frac)])









if __name__ == "__main__": 
    data_collection()



    




