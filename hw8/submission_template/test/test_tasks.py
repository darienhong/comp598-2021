import unittest
from pathlib import Path
import os, sys
import json
parentdir = Path(__file__).parents[1]
sys.path.append(parentdir)
from src.compile_word_counts import compute_word_count_dic
import src.compile_word_counts as compute_word_counts
import src.compute_pony_lang as compute_pony_lang 


class TasksTest(unittest.TestCase):
    def setUp(self):
        dir = os.path.dirname(__file__)
        self.mock_dialog = os.path.join(dir, 'fixtures', 'mock_dialog.csv')
        self.true_word_counts = os.path.join(dir, 'fixtures', 'word_counts.true.json')
        self.true_tf_idfs = os.path.join(dir, 'fixtures', 'tf_idfs.true.json')
        self.stopwords_path =  os.path.join(parentdir, 'data', 'stopwords.txt')

    def test_task1(self):
        with open(self.mock_dialog, 'r') as f1, open(self.true_word_counts, 'r') as f2: 
            twc = json.load(f2)
            output = compute_word_count_dic(f1, self.stopwords_path)
     
        self.assertEqual(output, twc)

    def test_task2(self):
        # use self.true_word_counts self.true_tf_idfs; REMOVE self.assertTrue(True) and write your own assertion, i.e. self.assertEquals(...)
        self.assertTrue(True)
        
    
if __name__ == '__main__':
    unittest.main()