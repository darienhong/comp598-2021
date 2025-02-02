# -*- coding: utf-8 -*-
"""data_analysis.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1-j0Q9Ppj7l_e-ivXEktH1-8a2T-z_Otl
"""

from google.colab import drive
drive.mount('/content/drive')

"""# Import Data"""

import os, sys
import json
import csv
import pandas as pd
import string
import re
import math

import matplotlib.pyplot as plt

#get stop words
stopwords = []
with open('/content/drive/My Drive/comp598final/stopwords.txt', 'r') as f:
  lines = f.read().splitlines()
  for line in lines:
    if str(line).startswith('#'):
      continue
    stopwords.append(line)

#get files and merge
# df = pd.read_csv('/content/drive/My Drive/comp598final/df1_annotated.csv')
df1 = pd.read_csv('/content/drive/My Drive/comp598final/df1_annotated.csv')
df2 = pd.read_csv('/content/drive/My Drive/comp598final/df2_annotated.csv')
df3 = pd.read_csv('/content/drive/My Drive/comp598final/df3_annotated.csv')
df = pd.concat([df1, df2, df3])

"""# Calculate tf-idf"""

#function for calculating tf-idf
#6 topics in total
def tf_idf(word, topic, script):
  #calculate tf-idf
  tf = int(script[topic][word])
  count = 0
  for topic in script.keys():
    if word in script[topic].keys():
      count = count + 1
  idf = math.log10(6/count)

  return tf*idf

#store number of words of each topic
count = dict()
count['public policies'] = dict()
count['vaccinations'] = dict()
count['quarantine'] = dict()
count['variants'] = dict()
count['impact on humans'] = dict()
count['political opinions'] = dict()
count['other'] = dict()

#count words
for index, row in df.iterrows():
  topic = row['Topic'].lower()
  if topic not in count.keys():
    continue

  dia = re.sub(r'[()\[\],-.?!:;#&]', ' ', str(row['Text']).lower())
  for word in dia.split():
    if not str.isalpha(word):
      continue
    if word not in stopwords:
      if word not in count[topic].keys():
        count[topic][word] = 1
      else:
        count[topic][word] = count[topic][word] + 1

#calculate tf-idf for each topic
#store scores
score = dict()

for topic in count.keys():
  #store tf-idf of each word for given ponytopic
  temp = dict()
  topic = topic.lower()

  #check whether is value in topic
  if not len(count[topic].keys()) == 0:
    for word in count[topic].keys():
      temp[word] = tf_idf(word, topic, count)
        
    #store the score
  score[topic] = temp

#get the top 10 and store in output
output = dict()
output['public policies'] = []
output['vaccinations'] = []
output['quarantine'] = []
output['variants'] = []
output['impact on humans'] = []
output['political opinions'] = []
output['other'] = []

for topic in score.keys():
  number = score[topic]
  #sort the dict
  n = 10
  if n > len(number.keys()):
    n = len(number.keys())
  sort = sorted(number, key=number.get, reverse=True)[:n]

  #store the words we need
  for word in sort:
    output[topic].append(word)

output

"""# Additional Analysis

1. frequency of each topic
"""

frequency = dict()

for index, row in df.iterrows():
  topic = row['Topic'].lower()
  if topic in frequency.keys():
    frequency[topic] = frequency[topic]+1
  else:
    frequency[topic] = 1

frequency

# plot
topics = []
height = []
for key in frequency.keys():
  topics.append(key)
  height.append(frequency[key])

#plt.bar(topics, height, width = 0.7)
plt.pie(height, labels = topics,
        startangle=90, shadow = True)
plt.title('topic engagement')

"""2. sentiment of each topic"""

#store sentiment for each topic
sentiment_sep = dict()
sentiment_sep['public policies'] = dict()
sentiment_sep['vaccinations'] = dict()
sentiment_sep['quarantine'] = dict()
sentiment_sep['variants'] = dict()
sentiment_sep['impact on humans'] = dict()
sentiment_sep['political opinions'] = dict()
sentiment_sep['other'] = dict()
for index, row in df.iterrows():
  topic = row['Topic'].lower()
  sen = row['Sentiment'].lower()

  if topic in sentiment_sep.keys():
    if sen in sentiment_sep[topic].keys():
      sentiment_sep[topic][sen] = sentiment_sep[topic][sen] + 1
    else:
      sentiment_sep[topic][sen] = 1

sentiment_sep

sense = []
pos = []
# plot for rate of positive
for key in sentiment_sep.keys():
  sense.append(key)
  if len(sentiment_sep.keys()) == 3:
    total = sentiment_sep[key]['positive'] + sentiment_sep[key]['negative'] + sentiment_sep[key]['neutral']
    per = sentiment_sep[key]['positive'] / total    
  else:
    if 'positive' not in sentiment_sep[key].keys():
      per = 0
    elif 'negative' not in sentiment_sep[key].keys():
      if 'neutral' not in sentiment_sep[key].keys():
        per = 1
      else:
        total = sentiment_sep[key]['positive'] + sentiment_sep[key]['neutral']
        per = sentiment_sep[key]['positive'] / total
    else:
      total = sentiment_sep[key]['positive'] + sentiment_sep[key]['negative']
      per = sentiment_sep[key]['positive'] / total
  pos.append(per)

plt.figure(figsize=(12,5))
plt.bar(sense, pos, width=0.7)

"""3. sentiment in total"""

sentiment = dict()
sentiment['neutral'] = 0
sentiment['positive'] = 0
sentiment['negative'] = 0
for index, row in df.iterrows():
  sen = row['Sentiment'].lower()
  sentiment[sen] = sentiment[sen]+1
print(sentiment)

sense = []
c = []
for key in sentiment.keys():
  sense.append(key)
  c.append(sentiment[key])

#todo: rm
c = [583, 71, 274]

plt.pie(c, labels = sense,
        startangle=90, shadow = True)
plt.title('sentiment of all relevant tweets')

"""## percentage of each sentiment"""

sents = dict()
sents['public policies'] = dict()
sents['vaccinations'] = dict()
sents['quarantine'] = dict()
sents['variants'] = dict()
sents['impact on humans'] = dict()
sents['political opinions'] = dict()
sents['other'] = dict()

for key in sents.keys():
  sents[key]['neutral'] = 0
  sents[key]['positive'] = 0
  sents[key]['negative'] = 0

for index, row in df.iterrows():
  sen = row['Sentiment'].lower()
  key = row['Topic'].lower()
  if key == 'irrelevant':
    continue
  sents[key][sen] = sents[key][sen]+1

#public policies
sense = []
c = []
for key in sents['public policies'].keys():
  sense.append(key)
  c.append(sents['public policies'][key])

print(sents['public policies'])

plt.pie(c, labels = sense,
        startangle=90, shadow = True)
plt.title('sentiment of tweets regarding public policies')

#vaccinations
sense = []
c = []
for key in sents['vaccinations'].keys():
  sense.append(key)
  c.append(sents['vaccinations'][key])

print(sents['vaccinations'])

plt.pie(c, labels = sense,
        startangle=90, shadow = True)
plt.title('sentiment of tweets regarding vaccinations')

#quarantine
sense = []
c = []
for key in sents['quarantine'].keys():
  sense.append(key)
  c.append(sents['quarantine'][key])

print(sents['quarantine'])

plt.pie(c, labels = sense,
        startangle=90, shadow = True)
plt.title('sentiment of tweets regarding quarantine')

#variants
sense = []
c = []
for key in sents['variants'].keys():
  sense.append(key)
  c.append(sents['variants'][key])

print(sents['variants'])

plt.pie(c, labels = sense,
        startangle=90, shadow = True)
plt.title('sentiment of tweets regarding variants')

#impact on humans
sense = []
c = []
for key in sents['impact on humans'].keys():
  sense.append(key)
  c.append(sents['impact on humans'][key])

print(sents['impact on humans'])

plt.pie(c, labels = sense,
        startangle=90, shadow = True)
plt.title('sentiment of tweets regarding impact on humans')

#political opinions
sense = []
c = []
for key in sents['political opinions'].keys():
  sense.append(key)
  c.append(sents['political opinions'][key])

print(sents['political opinions'])

plt.pie(c, labels = sense,
        startangle=90, shadow = True)
plt.title('sentiment of tweets regarding political opinions')

#other
sense = []
c = []
for key in sents['other'].keys():
  sense.append(key)
  c.append(sents['other'][key])
print(sents['other'])
plt.pie(c, labels = sense,
        startangle=90, shadow = True)
plt.title('sentiment of tweets regarding other')