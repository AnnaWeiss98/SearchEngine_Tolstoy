from tokenisation import Tokenizer
import shelve
import os

'''
Position stores data about the position of token
'''
class Position(object):
    '''
    Attributes: start - the first symbol of token,
    end - the symbol after the last token, string - the line where this token is
    '''
    def __init__(self, start, end, string):
        self.string = string
        self.start = start
        self.end = end
        
    @classmethod #bespeak to class, not to exemplar
    def from_token(cls, token, string):
        '''
        forcreating a class Position with token
        '''
        return cls(token.position, token.position + len(token.s), string)
    def __eq__(self, obj):
        '''
        check if two tokens are equal (it is so when they have the
        same first and last symbol
        '''
        return self.string==obj.string and self.start==obj.start and self.end == obj.end

        
class Indexer(object):
    '''
    Class Indexer allows to index files and write the indexes of tokens into a
    database. Every instance of class Indexer works with its own database.'''
    def __init__(self, path):
        self.db = shelve.open(path, writeback=True)

    def prescribe_index(self, path):
        if not isinstance(path, str):
            raise ValueError('Input has an unappropriate type,it should be str')
        
        tokenizer = Tokenizer()
        f = open(path, 'r')
        for i, string in enumerate(f):
            tokens = tokenizer.tokenize_generator_type(string)
            for token in tokens:
                if token.t == 'A' or token.t == 'D':
                    self.db.setdefault(token.s, {}).setdefault(path, []).append(Position.from_token(token, i))
        f.close()
                                                                            
    def __del__(self):
        self.db.close()
