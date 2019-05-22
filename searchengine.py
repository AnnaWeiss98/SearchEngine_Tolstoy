from tokenisation import Tokenizer
import shelve
import os


class TokenWindow(object):

    def __init__(self, allString ,toc, start, end):

        self.allString  = allString # строка в которой нашли токен полностью
        self.token = toc #  искомый токен
        self.win_start = start # начало окна
        self.win_end   = end # конец окна

    def __repr__(self):

        s= '{}, {}, {}, {}'.format(self.allString, self.token, self.win_start, self.win_end)

        return s


    def __eq__(self, obj):
        '''
        check if two tokens are equal (it is so when they have the
        same first and last symbol
        '''
        return self.token == obj.token and self.win_start==obj.win_start and self.win_end == obj.win_end


class SearchEngine(object):
    """
    Class containing methods for working with database.
    """
    def __init__(self, database):
        """
        Create an instance of SearchEngine class.
        """
        self.database = shelve.open(database)


    def __del__(self):
        self.database.close()


    def search(self, query):
        """
        Search database and return files
        and positions for the searched word
        """
        if not isinstance(query, str):
            raise ValueError
        return self.database.get(query, {})

    def multiple_search(self, query):
        if not isinstance(query, str):
            raise ValueError
        if not query:
            return {}

        tokenizer = Tokenizer()
        # tokenisation of query, create list of tokens
        searchlist = []
        for token in tokenizer.tokenize_generator_type(query):
            if token.t == 'A' or token.t == 'D':
                searchlist.append(token.s)
        # search each token from query
        results_of_search = []
        for token in searchlist:
            results_of_search.append(set(self.search(token)))
        # find files with all words from query
        list_of_files = results_of_search[0]
        for f in results_of_search:
            list_of_files = list_of_files & f
        # create a dictionary of positions of all query tokens in files
        final_dict ={}
        for f in list_of_files:
            final_dict[f] = []
            for token in searchlist:
                final_dict[f].extend(self.database[token][f])
            final_dict[f].sort()
        return final_dict


    def find_window(self, findstr, window_len):

        if not isinstance(findstr, str):
            raise ValueError
        if not findstr:
            return {}

        windows = {} 
        tokenizer = Tokenizer()  
        result_dict = self.multiple_search(findstr)  
        
        for file_key in result_dict.keys():
            wins = []
            result_list = result_dict[file_key]


            for result_token in result_list:

                with open(file_key) as f:
                   for i, line in enumerate(f):
                       if i == result_token.string: # i - the number that we are looking for
                            break
                line = line.strip("\n") # remove from line the symbol of transfer

                right_context = line[result_token.start:]
                left_context = line[:result_token.end][::-1] # overturned with a slice 

                i = 0
                for token in tokenizer.tokenize_generator_type(left_context):
                    if token.t in ['A','D']:
                       i+=1
                    if i == window_len:
                         break
                
                start = result_token.end - token.position - len(token.s)

                i = 0
                for token in tokenizer.tokenize_generator_type(right_context):
                    if token.t in ['A','D']:
                       i+=1
                    if i == window_len:
                         break

                end = result_token.start + token.position + len(token.s)
                wins.append (TokenWindow (line, result_token, start, end))
                                  
            if len(wins) > 0:
               windows[file_key] = wins
        		 
        return windows
