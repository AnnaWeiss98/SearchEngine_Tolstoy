import unittest
from tokenisation import Tokenizer
from collections import Generator


class TestMyCode (unittest.TestCase):
    # making a unit of Tokeniser class
    
    def setUp(self):
        self.x = Tokenizer()
    # the test itself
    
    def test_mygenerator_type(self):
        result = self.x.tokenize_generator_type(' h50 ht ? 20 h d sun')
        self.assertIsInstance(result, Generator)
        
    def test_type(self):
        result = list(self.x.tokenize_generator_type(' h50 ht ? 20 h d sun'))
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 15)
        self.assertEqual(result[0].s, ' ')
        self.assertEqual(result[0].t, 'S')
        self.assertEqual(result[14].s,'sun')
        self.assertEqual(result[14].t, 'A')
        
    def  test_MyError_type_number(self):
        with self.assertRaises(ValueError):
            list(self.x.tokenize_generator_type(12))
            
    def test_MyError_type_notList(self):
        s = [1, 2, 3, 'this is my string']
        with self.assertRaises(ValueError):
            list(self.x.tokenize_generator_type(s))   
            
    def test_mygenerator(self):
        result = self.x.tokenize_generator(' h50 ht ? 20 h d sun')
        self.assertIsInstance(result, Generator)
        
    def test_my_gen_begins_with_no_alpha(self):
        result=list(self.x.tokenize_generator(' h50 ht ? 20 h d sun'))
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 6)
        self.assertEqual(result[0].s, 'h')
        self.assertEqual(result[0].position, 1)
        self.assertEqual(result[1].s, 'ht')
        self.assertEqual(result[1].position, 5)
        
    def test_my_gen_begins_with_alpha(self):
        result=list(self.x.tokenize_generator('h50 ht ? 20 h d sun'))
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 6)
        self.assertEqual(result[0].s, 'h')
        self.assertEqual(result[0].position, 0)
        self.assertEqual(result[1].s, 'ht')
        self.assertEqual(result[1].position, 4)
        
    def test_my_gen_ends_with_no_alpha(self):
       result=list(self.x.tokenize_generator('h50 ht ? 20 h d sun'))
       self.assertIsInstance(result, list)
       self.assertEqual(len(result), 6)
       self.assertEqual(result[0].s, 'h')
       self.assertEqual(result[0].position, 0)
       self.assertEqual(result[4].s, 'sun')
       self.assertEqual(result[4].position, 16)
        
    def test_my_gen_ends_with_alpha(self):
        result=list(self.x.tokenize_generator('h50 ht ? 20 h d sun'))
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 6)
        self.assertEqual(result[0].s, 'h')
        self.assertEqual(result[0].position, 0)
        self.assertEqual(result[4].s, 'sun')
        self.assertEqual(result[4].position, 16)
        
    def test_MyError_number_gen(self):
        with self.assertRaises(ValueError):
            list(self.x.tokenize_generator(12))
            
    def test_MyError_notList_gen(self):
        s=[1, 2, 3, 'my name is Anya']
        with self.assertRaises(ValueError):
           list(self.x.tokenize_generator(s))

    def test_MyError_emptyString(self):
        result=self.x.tokenize('')
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 0)
            
    def test_begins_with_no_alpha(self):
        result=self.x.tokenize(' h50 ht ? 20 h d sun')
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 5)
        self.assertEqual(result[0].s, 'h')
        self.assertEqual(result[0].position, 1)
        self.assertEqual(result[1].s, 'ht')
        self.assertEqual(result[1].position, 5)
        
    def test_begins_with_alpha(self):
        result=self.x.tokenize('h50 ht ? 20 h d sun')
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 5)
        self.assertEqual(result[0].s, 'h')
        self.assertEqual(result[0].position, 0)
        self.assertEqual(result[1].s, 'ht')
        self.assertEqual(result[1].position, 4)
        
    def test_ends_with_no_alpha(self):
        result=self.x.tokenize(' h50 ht ? 20 h d sun')
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 5)
        self.assertEqual(result[0].s, 'h')
        self.assertEqual(result[0].position, 1)
        self.assertEqual(result[4].s, 'sun')
        self.assertEqual(result[4].position, 17)
        
    def test_ends_with_alpha(self):
        result=self.x.tokenize(' h50 ht ? 20 h d sun')
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 5)
        self.assertEqual(result[0].s, 'h')
        self.assertEqual(result[0].position, 1)
        self.assertEqual(result[4].s, 'sun')
        self.assertEqual(result[4].position, 17)
        
    def test_MyError_number(self):
        with self.assertRaises(ValueError):
            self.x.tokenize(12)
            
    def test_MyError_notList(self):
        s=[1, 2, 3, 'my name is Anya']
        with self.assertRaises(ValueError):
            self.x.tokenize(s)

    def test_MyError_emptyString(self):
        result=self.x.tokenize('')
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 0)
        
if __name__== '__main__':
    unittest.main()
