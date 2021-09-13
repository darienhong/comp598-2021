import pandas as pd 

def data_collection(): 
    data = pd.read_csv('../data/IRAhandle_tweets_1.csv', nrows=10000)
 
    # keep the tweets that are in english 
    isEnglish = data['language'] == 'English'
    data_english = data[isEnglish]
    print(data_english)
    isQuestion = ~data_english['content'].str.contains("?", regex=False)
    data_question = data_english[isQuestion]
    print(data_question)




if __name__ == "__main__": 
    data_collection()



    




