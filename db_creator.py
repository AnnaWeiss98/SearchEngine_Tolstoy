import io
import os
import shelve
from indexer import Position
from indexer import Indexer
from tokenisation import Tokenizer
from searchengine import SearchEngine


class Window_searcher():
    
    def __init__(self, database, window_len, files = None, path = None):
 
        self.files = files #  список файлов для анализа
        self.path = path   #  папка с текстовыми файлами
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


def main():

    Window_searcher('database',2,path='.\\docs\\')

if __name__ == "__main__":
    main()
