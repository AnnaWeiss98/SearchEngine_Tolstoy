from indexer import Indexer, Position
import unittest
import os


class IndexTest(unittest.TestCase):
    def setUp(self):
        self.x = Indexer("database")

    def test_not_file_name(self):
        with self.assertRaises(ValueError):
            self.x.prescribe_index(123)

    def test_open_file(self):
        with self.assertRaises(FileNotFoundError):
            self.x.prescribe_index('ed.txt')

    def test_database_created(self):
        file = open('test.txt', 'w')
        file.write('Baikal')
        file.close()
        self.x.prescribe_index('test.txt')
        '''
        The method listdir() returns a list containing the names of the entries in the directory given by path.
        '''
        files = os.listdir(path = ".")
        flag = False
        for f in files:
            if f.startswith('database.'):
                flag = True
            elif f.startswith('database'):
                if f == 'database':
                    flag = True
        self.assertEqual(flag, True)
        db_dict = dict(self.x.db)
        standart_result = {'Baikal':{'test.txt': [Position(0,6,0)]}}
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
        self.assertEqual(flag, True)
        db_dict = dict(self.x.db)
        standart_result = {'lake': {'test2.txt': [Position(12, 16, 0)]},
                           'a': {'test2.txt': [Position(10, 11, 0)]},
                           'is': {'test2.txt': [Position(7, 9, 0)]},
                           'Baikal': {'test2.txt': [Position(0, 6, 0)],
                           'test.txt': [Position(0, 6, 0)]}}
        self.assertEqual(db_dict, standart_result)
        os.remove('test2.txt')

    def tearDown(self):
        del self.x
        for f in os.listdir('.'):
            if f.startswith('database.'):
                os.remove(f)

if __name__== '__main__':
    unittest.main()
