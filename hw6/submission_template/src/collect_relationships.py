import bs4 as BeautifulSoup
import json 
import argparse
import requests
import os.path
import re


def get_args(): 
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', type=str)
    parser.add_argument('-o', '--output', type=str)

    return parser.parse_args().config, parser.parse_args().output

def load_config_file(config_file): 
    with open(config_file, 'r') as f: 
        cfg = json.load(f)
        dir_cache = cfg['cache_dir']
        target_people = cfg['target_people']

    return dir_cache, target_people

def collect_relationships(dir_cache, person, json_output): 
    if not os.path.isfile(f'{dir_cache}/{person}'): 
        open(f'{dir_cache}/{person}', 'wb').write(requests.get(f'https://www.whosdatedwho.com/dating/{person}').content)


    soup = BeautifulSoup(open(f'{dir_cache}/{person}', 'r', encoding='utf-8'), 'html.parser')
    div_person = soup.find('div', class_='ff-panel clearfix')

    h4_about = div_person.find('h4', class_='ff-auto-about')
    for item in h4_about.find_next_siblings():
        item.decompose()
    h4_about.decompose()

    # get a list of links & remove self-reference if needed
    list_regex = [*{a['href'] for a in div_person.find_all('a', href=True) if re.search('/dating/', str(a))}]
    if f'/dating/{person}' in list_regex:
        list_regex.remove(f'/dating/{person}')
    list_cleaned = [b.removeprefix('/dating/') for b in list_regex]
    json_output[person] = list_cleaned

def pretty_export(str_out, json_output):
    with open(str_out, 'w') as f_out:
        t = json.dumps(json_output, indent=4)
        t = re.sub('\[\n {7}', '[', t)
        t = re.sub('(?<!\]),\n {7}', ',', t)
        t = re.sub('\n {4}\]', ']', t)
        f_out.write(t)


def main(): 

    config_file, output_file = get_args()
    dir_cache, target_people = load_config_file(config_file)
    json_output = {}

    for person in target_people: 
        collect_relationships(dir_cache, person, json_output)

    pretty_export(output_file, json_output)

if __name__ == "__main__": 
    main() 