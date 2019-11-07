import unittest
from searchengine import SearchEngine,TokenWindow
from indexer import Position
import os

idealdict = {'sun': {'test_window_one.txt': [Position(0, 3, 0)]},
             'window': {'test_window_one.txt': [Position(4, 10, 0)]},
             'tree': {'test_window_one.txt': [Position(11, 15, 0)]},
             'apple': {'test_window_one.txt': [Position(16, 21, 0)]},
             'juse': {'test_window_one.txt': [Position(23, 27, 0)]},
             'border': {'test_window_one.txt': [Position(28, 34, 0)]},
             'films': {'test_window_one.txt': [Position(35, 40, 0)]},
             '23': {'test_window_one.txt': [Position(41, 43, 0)]},
             '45': {'test_window_one.txt': [Position(44, 46, 0)]},
             'good': {'test_window_one.txt': [Position(46, 50, 0)]},
             'Мы': {'test_window_two.txt': [Position(0, 2, 0)]},
             'тестируем': {'test_window_two.txt': [Position(3, 12, 0)]},
             'нашу': {'test_window_two.txt': [Position(13, 17, 0)]},
             'программу': {'test_window_two.txt': [Position(18, 27, 0)]},
             'для': {'test_window_two.txt': [Position(28, 31, 0)],
                     'test_window_three.txt': [Position(14, 17, 0),
                                               Position(14, 17, 1)]},
             'работы': {'test_window_two.txt': [Position(32, 38, 0)]},
             'с': {'test_window_two.txt': [Position(39, 40, 0)]},
             'окнами': {'test_window_two.txt': [Position(41, 47, 0)]},
             'Первая': {'test_window_three.txt': [Position(0, 6, 0)]},
             'строка': {'test_window_three.txt': [Position(7, 13, 0),
                                                  Position(7, 13, 1)]},
             'тестов': {'test_window_three.txt': [Position(18, 24, 0),
                                                  Position(18, 24, 1)]},
             'Вторая': {'test_window_three.txt': [Position(0, 6, 1)]}}

class WindowsTest (unittest.TestCase):

    def setUp(self):
        self.strr = 'sun window tree apple, juse border films 23 45good'
        #            01234567890123456789012345678901234567890123456789
        #            0         1         2         3         4
        self.strr2 = 'Мы тестируем нашу программу для работы с окнами. '
        #             01234567890123456789012345678901234567890123456789
        #             0         1         2         3         4
        self.strr3  = 'Первая строка для тестов.\n'
        #              01234567890123456789012345678901234567890123456789
        #              0         1         2         3         4

        self.strr4  = 'Вторая строка для тестов.'
        #              01234567890123456789012345678901234567890123456789
        #              0         1         2         3         4

        self.test_file = open('test_window_one.txt', 'w')
        self.test_file.write(self.strr)
        self.test_file.close()

        self.test_file = open('test_window_two.txt', 'w')
        self.test_file.write(self.strr2)
        self.test_file.close()

        self.test_file = open('test_window_three.txt', 'w')
        self.test_file.write(self.strr3)
        self.test_file.write(self.strr4)
        self.test_file.close()

        self.x = SearchEngine("test_db")
        self.x.database.update(idealdict)

    def tearDown(self):
        del self.x
        file_list = os.listdir(path=".")
        for i in file_list:
            if i == 'test_window_one.txt' or i == 'test_window_two.txt' or i == 'test_window_three.txt':
                os.remove(i)
            if i.startswith('test_db.'):
                os.remove(i)

    def test_wrong_input_error(self):  # instead of a line on input, user gives a list, so an error occurs
        with self.assertRaises(ValueError):
            files = ['test_window_one.txt']
            win = self.x.find_supplemented_window(files, 3,0,1,[(0,1)])

    def test_absent_key(self):
        result = self.x.find_supplemented_window('zzzz',1,0,1,[(0,1)])
        self.assertEqual(result, {})

    def test_empty_string(self):
        result = self.x.find_supplemented_window('',1,0,1,[(0,1)])
        self.assertIsInstance(result, dict)
        self.assertEqual(result, {})

    def test_get_window_begin(self):       
        result = self.x.find_supplemented_window('sun',1,0,1,[(0,1)])
        res = result['test_window_one.txt'][0]
        win = TokenWindow(self.strr, [Position(0, 3, 0)], 0, 50)
        ideal = {'test_window_one.txt': [win]}
        self.assertEqual(res.allString, win.allString)
        self.assertEqual(res, win)
        self.assertEqual(result, ideal)

    def test_get_window_simple(self):
        result = self.x.find_supplemented_window('tree', 2,0,1,[(0,1)])
        res = result['test_window_one.txt'][0]
        win = TokenWindow(self.strr, [Position(11, 15, 0)], 0, 50)
        ideal = {'test_window_one.txt': [win]}
        
        self.assertEqual(res.allString, win.allString)
        self.assertEqual(res, win)
        self.assertEqual(result, ideal)

    def test_get_window_end(self):
        result = self.x.find_supplemented_window('good', 1,0,1,[(0,1)])
        res = result['test_window_one.txt'][0]
        win = TokenWindow(self.strr, [Position(46, 50, 0)], 0, 50)
        ideal = {'test_window_one.txt': [win]}
        
        self.assertEqual(res.allString, win.allString)
        self.assertEqual(res, win)
        self.assertEqual(result, ideal)

    def test_get_window_simple2(self):
        result = self.x.find_supplemented_window('нашу', 2,0,1,[(0,1)])
        res = result['test_window_two.txt'][0]
        win = TokenWindow(self.strr2, [Position(13, 17, 0)], 0, 49)
        ideal = {'test_window_two.txt': [win]}
        
        self.assertEqual(res.allString, win.allString)
        self.assertEqual(res, win)
        self.assertEqual(result, ideal)


    def test_get_window_simple_two_line(self):
        result = self.x.find_supplemented_window('Вторая', 1,0,1,[(0,1)])
        res = result['test_window_three.txt'][0]
        win = TokenWindow(self.strr4, [Position(0, 6, 1)], 0, 25)
        ideal = {'test_window_three.txt': [win]}
       
        self.assertEqual(res.allString, win.allString)
        self.assertEqual(res, win)
        self.assertEqual(result, ideal)

    def test_get_window_two_result(self): # test returns two results
        result = self.x.find_supplemented_window('тестов', 1,0,1,[(0,2)])
        res1 = result['test_window_three.txt'][0]
        res2 = result['test_window_three.txt'][1]
        win1 = TokenWindow(self.strr3.replace('\n',''), [Position(18, 24, 0)], 0, 25)
        win2 = TokenWindow(self.strr4, [Position(18, 24, 1)], 0, 25)

        ideal = {'test_window_three.txt': [win1,win2]}

        self.assertEqual(res1.allString, win1.allString)
        self.assertEqual(res1, win1)
        self.assertEqual(res2.allString, win2.allString)
        self.assertEqual(res2, win2)
        self.assertEqual(result, ideal)

    def test_get_window_two_result2(self): # test returns only the first result
        result = self.x.find_supplemented_window('тестов', 1,0,1,[(0,1)])
        res1 = result['test_window_three.txt'][0]
        win1 = TokenWindow(self.strr3.replace('\n',''), [Position(18, 24, 0)], 0, 25)
        ideal = {'test_window_three.txt': [win1]}
        self.assertEqual(res1.allString, win1.allString)
        self.assertEqual(res1, win1)
        self.assertEqual(result, ideal)

    def test_get_window_two_result3(self): # test returns only the second result
        result = self.x.find_supplemented_window('тестов', 1,0,1,[(1,2)])
        res1 = result['test_window_three.txt'][0]
        win1 = TokenWindow(self.strr4.replace('\n',''), [Position(18, 24, 1)], 0, 25)
        ideal = {'test_window_three.txt': [win1]}
        self.assertEqual(res1.allString, win1.allString)
        self.assertEqual(res1, win1)
        self.assertEqual(result, ideal)



if __name__== '__main__':
    unittest.main()
