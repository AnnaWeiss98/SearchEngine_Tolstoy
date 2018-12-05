from Indexator import Indexator
import unittest
import os


class IndexTest(unittest.TestCase):
    def setUp(self):
        self.x = Indexator()
    def tearDown(self):
        files = os.listdir(path = ".")
         for f in files:
            if f.startswith('database.'):
                if f == 'database.dat':
                    os.remove(f)
                if f == 'database.dir':
                    os.remove(f)
                if f == 'database.bak':
                    os.remove(f)
            elif f.startswith('database'):
                if f == 'database':
                    os.remove(f)

    def test_not_file_name(self):
        with self.assertRaises(ValueError):
            self.x.prescribe_index(123)

    def test_open_file(self):
        with self.assertRaises(ValueError):
            self.x.prescribe_index('ed.txt')

    def test_database_created(self):
        file = open('test.txt', 'w')
        file.write('Baikal')
        file.close()
        self.x.prescribe_index('test.txt')
        #The method listdir() returns a list containing the names of the entries in the directory given by path.     
        files = os.listdir(path = ".")
        flag = False
        for f in files:
            if f.startswith('database.'):
                flag = True
            elif f.startswith('database'):
                if f == 'database':
                    flag = True
        self.assertTrue(flag)
        db_dict = dict(shelve.open(db_filename))
        standart_result = {'Baikal':{'test.txt': Position(0,6)}}
        self.assertEqual(db_dict, standart_result)
        os.remove('test.txt')

    def test_database_continued(self):
        file = open('test2.txt', 'w')
        file.write('Baikal is a lake')
        file.close()
        self.x.prescribe_index('test2.txt')
        files = os.listdir(path = ".")
        flag = False
        for f in files:
            if f.startswith('database.'):
                flag = True
            elif f.startswith('database'):
                if f == 'database':
                    flag = True
        self.assertTrue(flag)
        db_dict = dict(shelve.open(db_filename))
        standart_result = {'lake': {'test2.txt': Position(12, 16)},
                           'a': {'test2.txt': Position(10, 11)},
                           'is': {'test2.txt': Position(7, 9)},
                           'Baikal': {'test2.txt': Position(0, 6),
                           'test.txt': Position(0, 6)}}
        self.assertEqual(db_dict, standart_result)
        os.remove('test2.txt')
        #helloworld
