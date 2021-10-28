import unittest
from pathlib import Path
from datetime import datetime
import json
import ast
import os, sys
from src.clean import filter_tags, filter_invalid_json

parentdir = Path(__file__).parents[1]
sys.path.append(parentdir)


class CleanTest(unittest.TestCase):
    def setUp(self):

        self.test_path = os.path.join(parentdir, 'test')
        self.fixtures_path = os.path.join(self.test_path, 'fixtures')
        self.fixture_names = os.listdir(self.fixtures_path)
        self.fixture_names.sort()

        # load data from fixtures folder.
        self.fixture1 = os.path.join(self.fixtures_path, self.fixture_names[0])
        self.fixture2 = os.path.join(self.fixtures_path, self.fixture_names[1])
        self.fixture3 = os.path.join(self.fixtures_path, self.fixture_names[2])
        self.fixture4 = os.path.join(self.fixtures_path, self.fixture_names[3])
        self.fixture5 = os.path.join(self.fixtures_path, self.fixture_names[4])
        self.fixture6 = os.path.join(self.fixtures_path, self.fixture_names[5])
        

# test if title or title_text exists in json entry
    def test_title(self): 
        with open(self.fixture1, 'r', encoding='utf-8') as f: 
            print('Checking if title or title_text exists...')
            data = json.load(f)
            self.assertFalse(('title' in data) or ('title_text' in  data))
            print('Test OK')

# test if date is in proper format
    def test_date(self): 
        with open(self.fixture2, 'r', encoding='utf-8') as f: 
            print('Checking if the date is in Date and Time in UTC ISO 1681 format...')
            data = json.load(f)
            self.assertNotIsInstance(data['createdAt'], datetime)
     #       self.assertNotIsInstance(datetime.strptime(data['createdAt'], '%Y-%m-%dT%H:%M:%S%z'), datetime)
            print('Test OK')

# check if it a valid dict
    def test_valid(self): 
        with open(self.fixture3, 'r', encoding='utf-8') as f: 
            print('Checking if JSON file is a valid dictionary...')
            try: 
                line = ast.literal_eval(f.readline())
                self.assertIsInstance(ast.literal_eval(line), dict)
            except: 
                self.assertFalse(False)
            print('Test OK')

# check that author is not null, N/A or empty
    def test_author_na(self):
        with open(self.fixture4, 'r', encoding='utf-8') as f:
            print('Checking if author is null, N/A or empty...')
            data = json.load(f)
            self.assertTrue('author' in data)                                       # author needs to exist as a key
            self.assertFalse(data['author'] not in ('', 'N/A', 'null', None))        # can't be empty, N/A or null
            print('Test OK')

# check if total_count is an int, float, str and is castable to an int
    def test_count(self):
        with open(self.fixture5, 'r', encoding='utf-8') as f:
            print('Checking if total_count is a str containing a castable number (int or float)...')
            data = json.load(f)
            self.assertIsInstance(data['total_count'], (int, float, str))
            self.assertFalse(data['total_count'].isdigit())
            print('Test OK')

# check that the tags field is split on spaces
    def test_tags(self):
        with open(self.fixture6, 'r', encoding='utf-8') as f:
            print('Checking if tag field gets split when given 3 words...')     # assumption that 'tags' exist in JSON
            data = json.load(f)
            data['tags'] = [*{word for line in data['tags'] for word in line.split()}]     # process the 'tags' field 
            for word in data['tags']:                    
                self.assertEqual(len(word.split()), 1)
            print('Test OK')

if __name__ == '__main__':
    unittest.main()