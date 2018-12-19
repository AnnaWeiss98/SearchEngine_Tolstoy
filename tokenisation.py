"""
tokenizer
this module performs tokenisation of a text and extracts tokens
"""
import unicodedata #this is a module


class Token(object):  # example, part of token's klass
   
    """
    Class of tokens taken from a given text
    """
    def __init__(self,position,s):  # constructor, self-object,others atr
        """
        Constructor for token.
        @param position: position is an index of the first element of token
        @param s: s is a presentation of token's string
        @return: token
        """
        self.position = position  # token's position in the text
        self.s = s  # write the meaning of variable
        
    def __repr__(self):
        """
        a function that asign numbers to tokens
        """
        return self.s+'_'+str(self.position)


class Token_1 (Token):  # example, part of token's klass
    """
    Class of tokens taken from a given text
    """
    def __init__(self,position,s,t):  # constructor, self-object,others atr
        """
        Constructor for token.
        @param position: position is an index of the first element of token
        @param s: s is a presentation of token's string
        @return: token
        """
        self.position = position  # token's position in the text
        self.s = s  # write the meaning of variable
        self.t = t # type
    def __repr__(self):
        """
        a function that asign numbers to tokens
        this function returns token and its type
        """
        
        return self.s+'_'+str(self.t)
    
   
class Tokenizer(object):
    
    """
    Class that makes a list of tokens
    """
    def tokenize(self,strim):
        """
        A function that returns tokens with alphabetic symbols
        @param: strim of text
        @return: a list of tokens
        """
        if not isinstance(strim,str):
            raise ValueError('Input has an unappropriate type,it should be str')
        tokensback = []  # clean list
        if not strim: 
            return tokensback
        position = 0
        if strim[0].isalpha():
            inToken = True
        else:
            inToken = False
        for i,c in enumerate(strim):
            if c.isalpha()and not strim[i-1].isalpha():
                position=i
                inToken = True
            if not c.isalpha()and strim[i-1].isalpha() and inToken:
                s = strim[position:i]  # срез
                t = Token(position,s)  
                tokensback.append(t)  # writing token to list
                inToken = False
        """
        condition for alphabetic symbol standing without nonalphabetic symbol after it
        it is important for the end of text
        """
        if c.isalpha():
            s = strim[position:i+1]     
            t = Token(position,s)
            tokensback.append(t)
        return tokensback
        if c.isalpha():
            s = strim[position:i-1]     
            t = Token(position,s)
            tokensback.append(t)
        return tokensback

    def tokenize_generator(self,strim):
        """
        A function that returns tokens with alphabetic symbols
        @param: strim of text
        @return: a list of tokens
        """
        if not isinstance(strim,str):
            raise ValueError('Input has an unappropriate type,it should be str')
        position=0
        if strim[0].isalpha():
            inToken = True
        else:
            inToken = False
        for i,c in enumerate(strim):
            if c.isalpha()and not strim[i-1].isalpha():
                position = i
                inToken=True
            if not c.isalpha()and strim[i-1].isalpha() and inToken:
                s = strim[position:i]  # срез
                t = Token(position,s)  
                yield t  # writing token 
                inToken = False
        """
        condition for alphabetic symbol standing without nonalphabetic symbol after it
        it is important for the end of text
        """
        if c.isalpha():
            s = strim[position:i+1]     
            t = Token(position,s)
            yield t
        if c.isalpha():
            s = strim[position:i-1]     
            t = Token(position,s)
            yield t
            
    @staticmethod
    def get_type(c):
       """
       this function defines the type
       """
       if c.isalpha():
           p = 'A'
       if c.isdigit():
           p = 'D'
       if c.isspace():
           p = 'S'
           # we are looking for spaces
           #(punctuation)
       if unicodedata.category(c)[0]=='P':
           p = 'P'
       return p
    
    def tokenize_generator_type(self,strim):
        """
        A function that returns tokens with alphabetic symbols
        @param: strim of text
        @return: a list of tokens
        """
        if not isinstance(strim,str):
            raise ValueError('Input must be str !')
        position = 0
        last_type = ""
        for i,c in enumerate(strim):
            this_type = self.get_type(c) 
            if this_type != last_type and i>0:
                s = strim[position:i]  # representation of string
                t = Token_1(position,s,last_type)  
                yield t
                position=i
            last_type=this_type
        """
        condition for alphabetic symbol standing without nonalphabetic symbol after it
        it is important for the end of text
        """
        s = strim[position:i+1]
        t = Token_1(position,s,this_type)
        yield t

        
def main():
    x = Tokenizer()
    for i in x.tokenize_generator_type(' h50 ht ? 20 h d sun'):
        print(i)

if __name__ == "__main__":
    main()
