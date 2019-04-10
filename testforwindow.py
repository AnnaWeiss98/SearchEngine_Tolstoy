import unittest
from tokenwindow import Windows,TokenWindow
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
            if i == 'test_window_one.txt' or i == 'test_window_two.txt' or i == 'test_window_three.txt':
                os.remove(i)

    def test_wrong_input_error(self):
        with self.assertRaises(ValueError):
            files = ['test_window_one.txt']
            win = Windows(files, 'database', 2)
            result = win.find_window(123)

    def test_absent_key(self):
        files = ['test_window_one.txt']
        win = Windows(files, 'database', 2)
        result = win.find_window('zzzz')
        self.assertEqual(result, {})

    def test_empty_string(self):
        files = ['test_window_one.txt']
        win = Windows(files, 'database', 2)
        result = win.find_window('')
        self.assertIsInstance(result, dict)
        self.assertEqual(result, {})

    def test_get_window_begin(self):
        files = ['test_window_one.txt']
        winn = Windows(files, 'database', 1)
        res = winn.find_window('sun')
        self.assertEqual(len(res['test_window_one.txt']),1)
        result = res['test_window_one.txt'][0]
        win = TokenWindow(self.strr, Position(0, 3, 0),[Position(4, 10, 0)])
        win.normalize()
        self.assertEqual(result.allString, win.allString)
        self.assertEqual(result.token[0], win.token[0])
        self.assertEqual(result.win_start, win.win_start)
        self.assertEqual(result.win_end, win.win_end)
        self.assertEqual(result, win)

    def test_get_window_simple(self):
        files = ['test_window_one.txt']
        winn = Windows(files, 'database', 2)
        res = winn.find_window('tree')
        self.assertEqual(len(res['test_window_one.txt']),1)
        result = res['test_window_one.txt'][0]
        win = TokenWindow(self.strr, Position(11, 15, 0),[Position(0, 3, 0), Position(4, 10, 0), Position(16, 21, 0), Position(23, 27, 0)])
        win.normalize()
        self.assertEqual(result.allString, win.allString)
        self.assertEqual(result.token[0], win.token[0])
        self.assertEqual(result.win_start, win.win_start)
        self.assertEqual(result.win_end, win.win_end)
        self.assertEqual(result, win)

    def test_get_window_end(self):
        files = ['test_window_one.txt']
        winn = Windows(files, 'database', 1)
        res = winn.find_window('good')
        self.assertEqual(len(res['test_window_one.txt']),1)
        result = res['test_window_one.txt'][0]
        win = TokenWindow(self.strr, Position(46, 50, 0),[Position(44, 46, 0)])
        win.normalize()
        self.assertEqual(result.allString, win.allString)
        self.assertEqual(result.token[0], win.token[0])
        self.assertEqual(result.win_start, win.win_start)
        self.assertEqual(result.win_end, win.win_end)
        self.assertEqual(result, win)


    def test_get_window_for_two_word(self):
        files = ['test_window_one.txt']
        winn = Windows(files, 'database', 1)
        res = winn.find_window('tree juse')
        self.assertEqual(len(res['test_window_one.txt']),1)
        result = res['test_window_one.txt'][0]
        win = TokenWindow(self.strr, [Position(11, 15, 0) , Position(23, 27, 0)],[Position(4, 10, 0), Position(16, 21, 0), Position(16, 21, 0) ,Position(28, 34, 0)])
        win.normalize()
        self.assertEqual(result.allString, win.allString)
        self.assertEqual(result.token[0], win.token[0])
        self.assertEqual(result.win_start, win.win_start)
        self.assertEqual(result.win_end, win.win_end)
        self.assertEqual(result, win)


    def test_get_window_simple2(self): 
        files = ['test_window_two.txt']
        winn = Windows(files, 'database', 2)
        res = winn.find_window('нашу')
        self.assertEqual(len(res['test_window_two.txt']),1)
        result = res['test_window_two.txt'][0]
        win = TokenWindow(self.strr2, Position(13, 17, 0),[Position(0, 2, 0), Position(3, 12, 0), Position(18, 27, 0), Position(28, 31, 0)])
        win.normalize()
        self.assertEqual(result.allString, win.allString)
        self.assertEqual(result.token[0], win.token[0])
        self.assertEqual(result.win_start, win.win_start)
        self.assertEqual(result.win_end, win.win_end)
        self.assertEqual(result, win)


    def test_get_window_simple_two_line(self):
        files = ['test_window_three.txt']
        winn = Windows(files, 'database', 1)
        res = winn.find_window('Вторая')
        self.assertEqual(len(res['test_window_three.txt']),1)
        result = res['test_window_three.txt'][0]
        win = TokenWindow(self.strr4, Position(0, 6, 1),[Position(7, 13, 1)])
        win.normalize()
        self.assertEqual(result.allString, win.allString)
        self.assertEqual(result.token[0], win.token[0])
        self.assertEqual(result.win_start, win.win_start)
        self.assertEqual(result.win_end, win.win_end)
        self.assertEqual(result, win)

if __name__== '__main__':
    unittest.main()
