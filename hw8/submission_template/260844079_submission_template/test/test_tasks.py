import unittest
from pathlib import Path
import os, sys
import json
parentdir = Path(__file__).parents[1]
sys.path.append(parentdir)
from src.compile_word_counts import compute_word_count_dic
from src.compute_pony_lang import compute_tf_idf


class TasksTest(unittest.TestCase):
    def setUp(self):
        dir = os.path.dirname(__file__)
        self.mock_dialog = os.path.join(dir, 'fixtures', 'mock_dialog.csv')
        self.true_word_counts = os.path.join(dir, 'fixtures', 'word_counts.true.json')
        self.true_tf_idfs = os.path.join(dir, 'fixtures', 'tf_idfs.true.json')
        self.stopwords_path =  os.path.join(parentdir, 'data', 'stopwords.txt')

# test compile_word_counts compiles the correct word counts 
    def test_task1(self):
        print(f"Ensure compile_word_counts.py compiles the proper word counts")
        with open(self.mock_dialog, 'r') as f1, open(self.true_word_counts, 'r') as f2: 
            twc = json.load(f2)
            output = compute_word_count_dic(f1, self.stopwords_path)
        self.assertEqual(output, twc)
        print("OK")

# test compute_pony_lang computes the correct tf-idfs
    def test_task2(self):
        print(f"\nEnsure compute_pony_lang.py computes the proper tf-idf values")
        with open(self.true_word_counts, 'r') as f1, open(self.true_tf_idfs, 'r') as f2:
            twc = json.load(f1)
            true_tf_idfs = json.load(f2)
            output = compute_tf_idf(twc)
        self.assertEqual(output, true_tf_idfs)
        print("OK")
        
    
if __name__ == '__main__':
    unittest.main()