import json 
import os 
import argparse
from requests.auth import HTTPBasicAuth
import requests

def get_args(): 
    parser = argparse.ArgumentParser() 
    parser.add_argument('-o', '--output', type=str)
    parser.add_argument('-s', '--subreddit', type=str)

    return parser.parse_args().output, parser.parse_args().subreddit

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

def collect_reddit_posts(subreddit, headers): 
    post_request = requests.get(f'https://oauth.reddit.com/r/{subreddit}/new?limit=100', headers=headers)
    new_posts = post_request.json()['data']['children']
    return new_posts

def save_json(new_posts, output_file): 
    with open(output_file, 'w') as f: 
        for i in range(len(new_posts)):
            f.write(f'{json.dumps(new_posts[i])}\n')


def main(): 
    output_file, subreddit = get_args()
    headers = get_oauth() 
    new_posts = collect_reddit_posts(subreddit, headers)
    save_json(new_posts, output_file)


if __name__ == "__main__": 
    main() 
    





