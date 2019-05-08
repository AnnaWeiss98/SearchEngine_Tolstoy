import io, os
import shelve
from indexer import Position
from indexer import Indexer
from searchengine import SearchEngine

class TokenWindow(object):
    """
    konstructor
    """
    def __init__(self, allString ,toc, start, end):

        self.allString  = allString # string with required token
        self.token = toc #  required token
        self.win_start = start
        self.win_end   = end

    """
    The function will be called when accessing an instance of a
    class, for example. print(TokenWindow) 
    """
    def __repr__(self):

        s= '{}, {}, {}, {}'.format(self.allString, self.token, self.win_start, self.win_end)
        """
        return string for output
        """
        return s


    def __eq__(self, obj):
        '''
        check if two tokens are equal (it is so when they have the
        same first and last symbol)
        '''
        return self.token == obj.token and self.win_start==obj.win_start and self.win_end == obj.win_end


class Window_searcher(object):
    """
    Class with methods for searching windows in files from a list
    """

    """
    Constructor (method that creates an instance of the class)
     Input Parameters: File List, Token Base, Window Width
    """
    def __init__(self, files, database, window_len):

        self.files = files #list of files for analysis
        self.db = database
        self.window_len = window_len

        for path in self.files:
            indexator = Indexer(self.db+'.'+path)
            indexator.prescribe_index_v2(path)
            del indexator
         

    def __del__(self):  # Class destructor
      self.del_db()

    def  del_db (self):

        file_list = os.listdir(path=".")
        for i in file_list:
            if i == self.db:
                database_exists = True
                os.remove(i)
            elif i.startswith(self.db+'.'):
                database_exists = True
                os.remove(i)


    """
    Multi word search function
    """
    def find_window(self, findstr):

        if not isinstance(findstr, str):
            raise ValueError
        if not findstr:
            return {}

        windows = {}

        for path in self.files:
            wins = []
            search = SearchEngine(self.db+'.'+path)

            f = open(path, 'r')
            file_lines = f.readlines()
            f.close()
                          
            search_dict = search.multiple_search(findstr)
            if len(search_dict) == 0:
               self.del_db()
               continue

            search_tokens = list(search_dict.values())

            for s in search_tokens:
                for st in s:
                    list_tokens = []
                    for t in (list(search.database.values())):
                          if st.string in t.keys():
                                list_tokens.extend(t[st.string])
                    list_tokens.sort()  

                    indx = list_tokens.index(st) 

                    # calculate the beginning and end of the window
                    sta = indx - self.window_len if (indx - self.window_len) > 0 else 0
                    en = indx + self.window_len if (self.window_len + indx) < len(list_tokens) else -1
                    wins.append ( TokenWindow (file_lines[st.string], st, list_tokens[sta].start, list_tokens[en].end) )


            if len(wins) > 0:
               windows[path] = wins
        		 
        return windows


def main():

    #files = ['test.txt']
    files = ['tolstoy4.txt']
    win = Window_searcher(files, 'database', 2)
    while True:
        findstr = input("Слово для поиска: ")
        if findstr == "exit":
            break

        res = win.find_window(findstr)
        for v in res.values():
            print (v)

if __name__ == "__main__":
    main()
