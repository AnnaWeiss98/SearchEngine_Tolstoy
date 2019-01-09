import unittest
from searchengine import SearchEngine
from indexer import Position
import shelve
import os

file1 = " The Earth is round"
file2 = " The sun is round"
idealdict = {'sun': {'file2.txt': [Position(5, 8, 0)]},
             'The': {'file1.txt': [Position(1, 4, 0)],
                     'file2.txt': [Position(1, 4, 0)]},
             'Earth': {'file1.txt': [Position(5, 10, 0)]},
             'round': {'file1.txt': [Position(14, 19, 0)],
                       'file2.txt': [Position(12, 17, 0)]},
             'is': {'file1.txt': [Position(11, 13, 0)],
                                                                                                                                                                                                                             'file2.txt': [(9, 11, 0)]}}

class TestMySearchEngine (unittest.TestCase):

    def setUp(self):
        self.x = SearchEngine("database")
        self.x.database.update(idealdict)

    def test_searchengine_type(self):
        result = self.x.search("round")
        self.assertIsInstance(result, dict)

    def test_MyError_type_number(self):
        with self.assertRaises(ValueError):
           self.x.search(15) 

    def test_empty_string(self):
        result = self.x.search('')
        self.assertIsInstance(result, dict)
        self.assertEqual(result, {})

    def test_search_by_token(self):
        result = self.x.search('The')
        self.assertIsInstance(result, dict)
        self.assertEqual(result, idealdict['The'])

    def tearDown(self):
        del self.x
        for f in os.listdir('.'):
            if f.startswith('database.'):
                os.remove(f)

class TestForMultiWordSearch (unittest.TestCase):

    def setUp(self):
        self.x = SearchEngine("database")
        self.x.database.update(idealdict)

    def test_searchengine_type(self):
        result = self.x.multiple_search("round")
        self.assertIsInstance(result, dict)

    def test_MyError_type_number(self):
        with self.assertRaises(ValueError):
           self.x.multiple_search(15) 

    def test_empty_string(self):
        result = self.x.multiple_search('')
        self.assertIsInstance(result, dict)
        self.assertEqual(result, {})

    def test_search_by_token(self):
        result = self.x.multiple_search('The')
        self.assertIsInstance(result, dict)
        self.assertEqual(result, idealdict['The'])

    def test_search_two_tokens(self):
        result = self.x.multiple_search('The sun')
        self.assertIsInstance(result, dict)
        self.assertEqual(result, {'file2.txt': [Position(1, 4, 0),
                                                Position(5, 8, 0)]})

    def tearDown(self):
        del self.x
        for f in os.listdir('.'):
            if f.startswith('database.'):
                os.remove(f)
                
if __name__== '__main__':
    unittest.main()
