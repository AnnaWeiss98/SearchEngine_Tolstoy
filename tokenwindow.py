import io
import os
import shelve
from indexer import Position
from indexer import Indexer
from tokenisation import Tokenizer
from searchengine import SearchEngine

class TokenWindow(object):
    """
    konstructor
    """
    def __init__(self, allString ,toc, start, end):
        """
        The function will be called when accessing an instance of a
        class, for example. print(TokenWindow) 
        """
        self.allString  = allString # string with required token
        self.token = toc #  required token
        self.win_start = start 
        self.win_end   = end

    def __repr__(self):
        
        s= '{}, {}, {}, {}'.format(self.allString, self.token, self.win_start, self.win_end)
        """
        return string for output
        """
        return s


    def __eq__(self, obj):
        '''
        check if two tokens are equal (it is so when they have the
        same first and last symbol
        '''
        return self.token == obj.token and self.win_start==obj.win_start and self.win_end == obj.win_end

class Window_searcher(SearchEngine):
    """
    Class with methods for searching windows in files from a list
    """
    
    def __init__(self, database, window_len, files = None, path = None):
        """
        Constructor (method that creates an instance of the class)
        Input Parameters: File List, Token Base, Window Width
        """

        self.files = files # list of files for analysis
        self.path = path   #  path (папка) with textfiles
        self.window_len = window_len
        self.db_name = database

        indexator = Indexer(self.db_name)
        
        file_list = []
        
        if self.files is not None:
           file_list.extend(self.files)

        if self.path is not None: 
           for f in os.listdir(path=self.path):
               file_list.append(self.path+f)

        for p in file_list:
            print ("Indexing file: ", p)    
            indexator.prescribe_index(p)
        del indexator

        SearchEngine.__init__(self, database)

         

    def __del__(self):  # Class destructor

        file_list = os.listdir(path=".")
        for i in file_list:
            if i == self.db_name:
                database_exists = True
                os.remove(i)
            elif i.startswith(self.db_name+'.'):
                database_exists = True
                os.remove(i)


    def find_window(self, findstr):
        """
        Multi word search function
        """
        if not isinstance(findstr, str):
            raise ValueError
        if not findstr:
            return {}

        windows = {} # return windows
        tokenizer = Tokenizer() # for tokenising the string from file
        result_dict = self.multiple_search(findstr)  # search
        
        for file_key in result_dict.keys():
            wins = []
            f = open(file_key, 'r')
            file_lines = f.readlines()
            
            result_list = result_dict[file_key]
            for result_token in result_list:

                position = result_token.start
                string_index = result_token.string
                token_list = [token for token in tokenizer.tokenize_generator_type(file_lines[string_index]) if token.t in ['A','D']]
                indx = 0 
                for token in token_list:
                   if token.position == position:
                        break
                   indx +=1

                if indx < len(token_list):                   
                     """
                     calculate the beginning and end of the window
                     """
                     sta = indx - self.window_len if (indx - self.window_len) > 0 else 0
                     en = indx + self.window_len if (self.window_len + indx) < len(token_list) else -1
                     wins.append (TokenWindow (file_lines[string_index], result_token, token_list[sta].position, token_list[en].position+len(token_list[en].s)))
                                  
 
            f.close()
                          
            if len(wins) > 0:
               windows[file_key] = wins
        		 
        return windows

def main():

    win = Window_searcher('database', 2, path='.\docs\\')
    while True:
        findstr = input("Слово для поиска: ")
        if findstr == "exit":
            break

        res = win.find_window(findstr)
        for k in res:
            print(k)
            for v in res[k]:
                print(v)

if __name__ == "__main__":
    main()
