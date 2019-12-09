import unittest
from searchengine import SearchEngine,TokenWindow
#from indexer import Position
#import os

class MASLsTest (unittest.TestCase):

    def setUp(self):
        self.x = SearchEngine()

    def tearDown(self):
        pass


    def test_list_empty(self):
        result = self.x.merge_and_sort_lists([])
        wanted = []
        self.assertEqual(list(result), wanted)


    def test_list_empty2(self):
        result = self.x.merge_and_sort_lists([[],[],[]])
        wanted = []
        self.assertEqual(list(result), wanted)


    def test_1_list_int(self):
        result = self.x.merge_and_sort_lists([[9,10,11]])
        wanted = [9,10,11]
        self.assertEqual(list(result), wanted)

    def test_2_list_int(self):
        result = self.x.merge_and_sort_lists([[1,2,3],[9,10,11]])
        wanted = [1,2,3,9,10,11]
        self.assertEqual(list(result), wanted)

    def test_3_list_int(self):
        result = self.x.merge_and_sort_lists([[1,2,3],[9,10,11],[4,5,6]])
        wanted = [1,2,3,4,5,6,9,10,11]
        self.assertEqual(list(result), wanted)

    def test_3_list_int_dif_len(self):
        result = self.x.merge_and_sort_lists([[1,2,3],[9,10,11,12,13,14,15],[4,5,6,7,8]])
        wanted = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
        self.assertEqual(list(result), wanted)

    def test_3_list_int_empty(self):
        result = self.x.merge_and_sort_lists([[1,2,3],[],[4,5,6,7,8]])
        wanted = [1,2,3,4,5,6,7,8]
        self.assertEqual(list(result), wanted)


    def test_1_list_abc(self):
        result = self.x.merge_and_sort_lists([['c','a','b']])
        wanted = ['c','a','b']
        self.assertEqual(list(result), wanted)


    def test_3_list_abc_dif_len(self):
        result = self.x.merge_and_sort_lists([['a','b','c'],['d','f','g','h']])
        wanted = ['a','b','c','d','f','g','h']
        self.assertEqual(list(result), wanted)



if __name__== '__main__':
    unittest.main()
