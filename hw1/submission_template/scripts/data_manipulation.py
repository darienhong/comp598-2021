import pandas as pd 
import numpy as np

def data_collection(): 
    data = pd.read_csv('../data/IRAhandle_tweets_1.csv', nrows=10000)
 
    # keep the tweets that are in english 
  
    data_english = data[data['language'] == 'English']
    print(data_english)
    data_question = data_english[~data_english['content'].str.contains("?", regex=False)]
    print(data_question)
    data_question.to_csv('new_data.tsv', sep='\t', index=False)

  #  contains_trump = data_question['content'].str.contains('[^a-zA-Z]Trump') or data['content'].str.contains('\s+Trump')
    data_question['trump_mention'] = np.where(data_question['content'].str.contains("Trump"), True, False)
    print(data_question)
    header = ["tweet_id", "publish_date", "content", "trump_mention"]
    data_question.to_csv('dataset.tsv', sep='\t', columns = header)






if __name__ == "__main__": 
    data_collection()



    




