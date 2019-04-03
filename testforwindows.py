import unittest
from tokenwindow import Windows
import os

s_sun='''sun window tree apple, juse border films 23 45good
[4, 11, 16] [1, 0, 2] 20'''

s_sun_films='''sun window tree apple, juse border films 23 45good
[4, 11, 16, 23, 28, 41, 44, 46] [1, 0, 2] [1, 35, 39] 49'''

idealdict = {'sun':  s_sun,
             'sun_films': s_sun_films}

class WindowsTest (unittest.TestCase):

    def setUp(self):
        self.x = Windows(['tests.txt'])

    def test_empty_string(self):
        result = self.x.search('')
        self.assertIsInstance(result, dict)
        self.assertEqual(result, {})

    def test_search_by_token(self):
        result = self.x.search('sun')
        self.assertIsInstance(result, dict)
        self.assertEqual(str(result['tests.txt'][0]), idealdict['sun'])

    def test_multiple_search_by_token(self):
        result = self.x.multiple_search('sun films')
        self.assertIsInstance(result, dict)
        self.assertEqual(str(result['tests.txt'][0]), idealdict['sun_films'])

if __name__== '__main__':
    unittest.main()
