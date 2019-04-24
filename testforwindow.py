import unittest
from tokenwindow import Window_searcher,TokenWindow
from indexer import Position
import os

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

    def tearDown(self):
        file_list = os.listdir(path=".")
        for i in file_list:
            if i in {'test_window_one.txt', 'test_window_two.txt', 'test_window_three.txt'}:
                os.remove(i)

    def test_wrong_input_error(self):
        with self.assertRaises(ValueError):
            files = ['test_window_one.txt']
            win = Window_searcher(files, 'database', 2)
            result = win.find_window(123)

    def test_absent_key(self):
        files = ['test_window_one.txt']
        win = Window_searcher(files, 'database', 2)
        result = win.find_window('zzzz')
        self.assertEqual(result, {})

    def test_empty_string(self):
        files = ['test_window_one.txt']
        win = Window_searcher(files, 'database', 2)
        result = win.find_window('')
        self.assertIsInstance(result, dict)
        self.assertEqual(result, {})

    def test_get_window_begin(self):
        files = ['test_window_one.txt']
        winn = Window_searcher(files, 'database', 1)
        res = winn.find_window('sun')
        self.assertEqual(len(res['test_window_one.txt']), 1)
        result = res['test_window_one.txt'][0]
        win = TokenWindow(self.strr,Position(0, 3, 0), 0, 10)
        self.assertEqual(result.allString, win.allString)
        self.assertEqual(result.token, win.token)
        self.assertEqual(result.win_start, win.win_start)
        self.assertEqual(result.win_end, win.win_end)
        self.assertEqual(result, win)

    def test_get_window_simple(self):
        files = ['test_window_one.txt']
        winn = Window_searcher(files, 'database', 2)
        res = winn.find_window('tree')
        self.assertEqual(len(res['test_window_one.txt']), 1)
        result = res['test_window_one.txt'][0]
        win = TokenWindow(self.strr, Position(11, 15, 0), 0, 27)
        self.assertEqual(result.allString, win.allString)
        self.assertEqual(result.token, win.token)
        self.assertEqual(result.win_start, win.win_start)
        self.assertEqual(result.win_end, win.win_end)
        self.assertEqual(result, win)

    def test_get_window_end(self):
        files = ['test_window_one.txt']
        winn = Window_searcher(files, 'database', 1)
        res = winn.find_window('good')
        self.assertEqual(len(res['test_window_one.txt']), 1)
        result = res['test_window_one.txt'][0]
        win = TokenWindow(self.strr, Position(46, 50, 0), 44, 50)
        self.assertEqual(result.allString, win.allString)
        self.assertEqual(result.token, win.token)
        self.assertEqual(result.win_start, win.win_start)
        self.assertEqual(result.win_end, win.win_end)
        self.assertEqual(result, win)


    def test_get_window_simple2(self):  #test for russian token
        files = ['test_window_two.txt']
        winn = Window_searcher(files, 'database', 2)
        res = winn.find_window('нашу')
        self.assertEqual(len(res['test_window_two.txt']), 1)
        result = res['test_window_two.txt'][0]
        win = TokenWindow(self.strr2, Position(13, 17, 0), 0, 31)
        self.assertEqual(result.allString, win.allString)
        self.assertEqual(result.token, win.token)
        self.assertEqual(result.win_start, win.win_start)
        self.assertEqual(result.win_end, win.win_end)
        self.assertEqual(result, win)


    def test_get_window_simple_two_line(self):
        files = ['test_window_three.txt']
        winn = Window_searcher(files, 'database', 1)
        res = winn.find_window('Вторая')
        self.assertEqual(len(res['test_window_three.txt']), 1)
        result = res['test_window_three.txt'][0]
        win = TokenWindow(self.strr4, Position(0, 6, 1), 0, 13)
        self.assertEqual(result.allString, win.allString)
        self.assertEqual(result.token, win.token)
        self.assertEqual(result.win_start, win.win_start)
        self.assertEqual(result.win_end, win.win_end)
        self.assertEqual(result, win)

if __name__== '__main__':
    unittest.main()
