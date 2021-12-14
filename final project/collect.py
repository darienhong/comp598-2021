# -*- coding: utf-8 -*-
"""Comp 598 final.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1NRxQazSAdSeNMYuNNt-GqAEy-FMoHlzM
"""

from google.colab import drive
drive.mount('/content/drive')

import sys
import time
import json
import pandas as pd
import tweepy
import datetime

consumer_key = "krJYOqUPjgEZGj84Q1aBG0F08"
consumer_secret = "20VpB3OORDh4HqV3d89p5uEUsetCFan2Dsr5MouIlRB5YCSTJB"
access_token = "1465795175297519623-zZXZEkdzwWC9ssD118sUEmA8eB26x8"
access_token_secret = "GABgQXhq8wtAaIJdlmUHQS9fRw5Uw9JETod83N2ijVeLW"

auth = tweepy.auth.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth,wait_on_rate_limit=True)

#count = 1000
#end_time = '2021-12-03'#datetime.datetime.now().strftime('%Y-%m-%d')
#start_time = (datetime.datetime.now() - datetime.timedelta(days = 3)).strftime('%Y-%m-%d')
text_query = '(COVID OR vaccination OR moderna OR pfizer OR vaccine OR zeneca OR janssen OR astra OR johnson&johnson OR covid-19 OR variant OR coronavirus OR quanrantine OR pandemic) -filter:retweets -filter:link'

#12-01
tweets1 = tweepy.Cursor(api.search,q=text_query, lang='en', until = '2021-12-02', tweet_mode = 'extended').items(300)
tweets_list1 = [[tweet.created_at, tweet.id, tweet.full_text] for tweet in tweets1]

#12-02
tweets2 = tweepy.Cursor(api.search,q=text_query, lang='en', until = '2021-12-03', tweet_mode = 'extended').items(300)
tweets_list2 = [[tweet.created_at, tweet.id, tweet.full_text] for tweet in tweets2]

#12-03
tweets3 = tweepy.Cursor(api.search,q=text_query, lang='en', until = '2021-12-04', tweet_mode = 'extended').items(400)
tweets_list3 = [[tweet.created_at, tweet.id, tweet.full_text] for tweet in tweets3]

tweets_df1 = pd.DataFrame(tweets_list1, columns=['Datetime', 'Tweet Id', 'Text'])

tweets_df2 = pd.DataFrame(tweets_list2, columns=['Datetime', 'Tweet Id', 'Text'])

tweets_df3 = pd.DataFrame(tweets_list3, columns=['Datetime', 'Tweet Id', 'Text'])

tweets_df1.to_csv('/content/drive/My Drive/comp598final/tweets1.csv')

tweets_df2.to_csv('/content/drive/My Drive/comp598final/tweets2.csv')

tweets_df3.to_csv('/content/drive/My Drive/comp598final/tweets3.csv')

# add column to record topic and sentiment
df1 = pd.DataFrame() 
df1['Topic']=['']*300
#sentiment is neutral by default
df1['Sentiment']=['neutral']*300
df1['Text']=tweets_df1['Text']

df1.to_csv('/content/drive/My Drive/comp598final/df1.csv')

df2 = pd.DataFrame() 
df2['Topic']=['']*300
#sentiment is neutral by default
df2['Sentiment']=['neutral']*300
df2['Text']=tweets_df2['Text']

df2.to_csv('/content/drive/My Drive/comp598final/df2.csv')

df3 = pd.DataFrame() 
df3['Topic']=['']*400
#sentiment is neutral by default
df3['Sentiment']=['neutral']*400
df3['Text']=tweets_df3['Text']

df3.to_csv('/content/drive/My Drive/comp598final/df3.csv')