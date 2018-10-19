import unittest
import tokenisation
from tokenisation import Tokenizer
from collections import Generator
class TestMyCode (unittest.TestCase):
    # making a unit of Tokeniser class
    def setUp(self):
        self.x = Tokenizer()
    # the test itself
    '''def test_MyTokenizer(self):
        result=self.x.tokenize(' h50 ht ? 20 h d sun)')
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 5)
        self.assertEqual(result[0].s, 'h')
        self.assertEqual(result[0].position, 1)'''
    def test_begins_with_no_alpha(self):
        result=list(self.x.tokenize(' h50 ht ? 20 h d sun)'))
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 5)
        self.assertEqual(result[0].s, 'h')
        self.assertEqual(result[0].position, 1)
        self.assertEqual(result[1].s, 'ht')
        self.assertEqual(result[1].position, 5)
    def test_begins_with_alpha(self):
        result=list(self.x.tokenize('h50 ht ? 20 h d sun)'))
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 5)
        self.assertEqual(result[0].s, 'h')
        self.assertEqual(result[0].position, 0)
        self.assertEqual(result[1].s, 'ht')
        self.assertEqual(result[1].position, 4)
    def test_ends_with_no_alpha(self):
        result=list(self.x.tokenize(' h50 ht ? 20 h d sun)'))
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 5)
        self.assertEqual(result[0].s, 'h')
        self.assertEqual(result[0].position, 1)
        self.assertEqual(result[4].s, 'sun')
        self.assertEqual(result[4].position, 17)
    def test_ends_with_alpha(self):
        result=list(self.x.tokenize(' h50 ht ? 20 h d sun'))
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 5)
        self.assertEqual(result[0].s, 'h')
        self.assertEqual(result[0].position, 1)
        self.assertEqual(result[4].s, 'sun')
        self.assertEqual(result[4].position, 17)
    def test_MyError_number(self):
        with self.assertRaises(ValueError):
            list(self.x.tokenize(12))
    def test_MyError_notList(self):
        s=[1, 2, 3, 'my name is Anya']
        with self.assertRaises(ValueError):
            list(self.x.tokenize(s))
if __name__== '__main__':
    unittest.main()
        
