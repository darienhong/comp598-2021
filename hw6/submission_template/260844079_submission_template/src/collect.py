''' 
Collect reddit data to compute the average title length
'''

import pandas as pd 
import requests
import json
from requests.auth import HTTPBasicAuth

# authorization
def get_oauth(): 
    auth = HTTPBasicAuth('mFecyUH7ruBJknmncKXg1g', 'U3RJ1i85JjdXy-IkZUsJtONxn0kPQw')
    data = {'grant_type': 'password', 'username': '598_temp_collector', 'password': 'mcgillcomp598'}

    # setup header info
    headers = {'User-Agent': 'comp598_collector/0.0.1'}

    # add authorization to our headers dictionary
    res = requests.post('https://www.reddit.com/api/v1/access_token', auth=auth, data=data, headers=headers)
    TOKEN = res.json()['access_token']
    headers = {**headers, **{'Authorization': f"bearer {TOKEN}"}}

    return headers 

# collect posts based on subreddits given
def collect_reddit_posts(subred_sub, subred_posts, headers): 
    subscriber_list = [] 
    post_list = []

    # collect 100 posts from each top ten subbed 
    for subreddit in subred_sub: 
        subscriber_list.append(requests.get(f'https://oauth.reddit.com/r/{subreddit}/new?limit=100', headers=headers).json()['data']['children'])

    # collect 100 posts from each top ten most popular (by posts)
    for subreddit in subred_posts: 
        post_list.append(requests.get(f'https://oauth.reddit.com/r/{subreddit}/new?limit=100', headers=headers).json()['data']['children'])

    return subscriber_list, post_list

# save data to json file
def export_json(file, data):
    with open(file,'w') as f: 
        for i in range (0, 10): 
            for j in range(0, 100):
                f.write(f'{json.dumps(data[i][j])}\n')


def main(): 
    # subreddits we want to extract from 
    subred_sub = ['funny', 'AskReddit', 'gaming', 'aww', 'pics', 'Music', 'science', 'worldnews', 'videos', 'todayilearned']
    subred_posts = ['AskReddit', 'memes', 'politics', 'nfl', 'nba', 'wallstreetbets', 'teenagers', 'PublicFreakout', 'leagueoflegends', 'unpopularopinion']

    # authenticate
    headers = get_oauth() 

    # collect the posts 
    subscriber_list, post_list = collect_reddit_posts(subred_sub, subred_posts, headers)

    # save the posts to json 
    export_json('../sample1.json', subscriber_list)
    export_json('../sample2.json', post_list)


if __name__ == "__main__": 
    main()

