from tokenisation import Tokenizer
import shelve
import os


class SearchEngine(object):
    """
    Class containing methods for working with database.
    """
    def __init__(self, database):
        """
        Create an instance of SearchEngine class.
        """
        self.database = shelve.open(database)

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

                  
       
