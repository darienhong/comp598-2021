import unittest
from pathlib import Path
import os, sys
import filecmp
parentdir = Path(__file__).parents[1]
sys.path.append(parentdir)
import src.compile_word_counts as compute_word_counts
import src.compute_pony_lang as compute_pony_lang 


class TasksTest(unittest.TestCase):
    def setUp(self):
        dir = os.path.dirname(__file__)
        self.mock_dialog = os.path.join(dir, 'fixtures', 'mock_dialog.csv')
        self.true_word_counts = os.path.join(dir, 'fixtures', 'word_counts.true.json')
        self.true_tf_idfs = os.path.join(dir, 'fixtures', 'tf_idfs.true.json')
        self.stopwords_path = os.path.join(parentdir, 'data', 'stopwords.txt')

    def test_task1(self):
        compute_word_counts.compute_with_args(self.mock_dialog, "output.json", self.stopwords_path)
        self.assertTrue(filecmp.cmp('output.json', self.true_word_counts))

    def test_task2(self):
        # use self.true_word_counts self.true_tf_idfs; REMOVE self.assertTrue(True) and write your own assertion, i.e. self.assertEquals(...)
        self.assertTrue(True)
        
    
if __name__ == '__main__':
    unittest.main()