import json 
import argparse
import ast
from datetime import datetime

def get_args(): 
    parser = argparse.ArgumentParser() 
    parser.add_argument('-i', '--input', type=str)
    parser.add_argument('-o', '--output', type=str)

    return parser.parse_args().input, parser.parse_args().output

# keep only the posts that are valid json dictionaries
def filter_invalid_json(input): 
    list_json = []
    with open(input, 'r') as f: 
        lines = f.readlines() 
        for i in range(len(lines)): 
            try: 
                line_dict = ast.literal_eval(lines[i])
                assert type(line_dict) is dict
                list_json.append(line_dict)
            except: 
                pass 
    return list_json

# filter total_count value
def filter_count(list_json): 
    key_val='total_count'
    for dict in list_json: 
        try: 
            if key_val in dict: 
                assert isinstance(dict[key_val], (int, float, str))
                dict[key_val] = int(float(dict[key_val]))
        except: 
            list_json.remove(dict)
    return list_json

# filter author value and remove those that are null, empty or N/A
def filter_author_valid(list_json): 
    key_val='author'
    for dict in list_json: 
        try: 
            assert key_val in dict 
            assert dict[key_val] not in ('', 'N/A', 'null', None)
        except: 
            list_json.remove(dict)

    return list_json

def filter_title(list_json): 
    key_val=('title', 'title_text')
    for dict in list_json: 
        try: 
            if key_val[0] in dict: 
                continue 
            elif key_val[1] in dict: 
                dict[key_val[0]] = dict.pop(key_val[1])
            else: 
                raise Exception
        except: 
            list_json.remove(dict)
    return list_json

def filter_tags(list_json): 
    key_val='tags'
    for dict in list_json: 
        if key_val in dict: 
            dict[key_val] = [*{word for line in dict[key_val] for word in line.split()}]
    return list_json

def filter_datetime(list_json): 
    key_val='createdAt'
    for dict in list_json: 
        try: 
             if key_val in dict: 
                 test = datetime.strptime(dict[key_val], '%Y-%m-%dT%H:%M:%S%z')
                 dict[key_val] = test.isoformat()
        except:
            list_json.remove(dict)
    return list_json


def main(): 

    # get script arguments 
    input_str, output_str = get_args()

    list_json = filter_invalid_json(input_str)
    list_json = filter_count(list_json)
    list_json = filter_author_valid(list_json)
    list_json = filter_title(list_json)
    list_json = filter_tags(list_json)
    list_json = filter_datetime(list_json)

    with open(output_str, 'w') as f:
        f.write('\n'.join(json.dumps(i) for i in list_json))


if __name__ == "__main__": 
    main()






        

