from tokenisation import Tokenizer
import shelve
import os
import re


class TokenWindow(object):
    def __init__(self, allString, pos, start, end):
        self.allString = allString  # all the line
        self.positions = pos  # list of Positions
        self.win_start = start  # start window
        self.win_end = end  # end window

    def __repr__(self):
        s = '{}, {}, {}, {}'.format(self.allString, str(self.positions), self.win_start, self.win_end)

        return s

    def __eq__(self, obj):
        '''
        check if two tokens are equal (it is so when they have the
        same first and last symbol
        '''
        return self.positions == obj.positions and self.win_start == obj.win_start and self.win_end == obj.win_end

    def window_is_junction(self, obj):
        return (self.win_start <= obj.win_end and
                self.win_end >= obj.win_start and
                obj.allString == self.allString)

    def get_BB_string(self):
        """
        Creates a string that represents context. Query words are 'highlighted'
        i.e. surrounded by HTML tags <b></b>.
        Returns:
            String cut to size of the context with query words highlighted.
        """
        result_string = self.allString[self.win_start:self.win_end]

        for position in reversed(self.positions):
            end = position.end - self.win_start
            start = position.start - self.win_start
            result_string = result_string[:end] + '</b>' + result_string[end:]
            result_string = result_string[:start] + '<b>' + result_string[start:]
        return result_string


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
        final_dict = {}
        for f in list_of_files:
            final_dict[f] = []
            for token in searchlist:
                final_dict[f].extend(self.database[token][f])
            final_dict[f].sort()
        return final_dict

    def multiple_search_lim(self, query, offset, limit):

        # with the limits for files

        if offset < 0:
           offset = 0 

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
        final_dict = {} 
        list_of_files= sorted(list_of_files)
        for i, f in enumerate(list_of_files):
           
            # key clipping
            if i >= offset + limit:
                break
            if i < offset:
                continue

            final_dict[f] = []
            for token in searchlist:
                final_dict[f].extend(self.database[token][f])
            final_dict[f].sort()
        return final_dict

    def find_window(self, findstr, window_len=3):
        """
        Search database and return files
        and positions for the searched word
        """

        if not isinstance(findstr, str):
            raise ValueError
        if not findstr:
            return {}

        windows = {}
        tokenizer = Tokenizer()
        result_dict = self.multiple_search(findstr)

        for file_key in result_dict:
            wins = []
            result_list = result_dict[file_key]

            for result_position in result_list:

                with open(file_key) as f:
                    for i, line in enumerate(f):
                        if i == result_position.string:
                            break
                line = line.strip("\n")

                right_context = line[result_position.start:]
                left_context = line[:result_position.end][::-1]

                for i, token in enumerate(tokenizer.generate_type_AD(left_context)):
                    if i == window_len:
                        break
                start = result_position.end - token.position - len(token.s)

                for i, token in enumerate(tokenizer.generate_type_AD(right_context)):
                    if i == window_len:
                        break
                end = result_position.start + token.position + len(token.s)

                wins.append(TokenWindow(line, [result_position], start, end))

            if len(wins) > 0:
                windows[file_key] = wins

        return self.join_windows(windows)

    def find_window_lim(self, findstr, window_len=3, offset=0, limit=0, winLimits=None):
        """
        Search database and return files
        and positions for the searched word
        witch limits and limits for file defined this function
        """

        if not isinstance(findstr, str):
            raise ValueError
        if not findstr:
            return {}

        windows = {}
        tokenizer = Tokenizer()
        result_dict = self.multiple_search(findstr)

        for f, file_key in enumerate(result_dict.keys()):
            wins = []
            if f >= offset + limit:
                break

            if f < offset:
                continue

            result_list = result_dict[file_key]

            if winLimits is not None:
                st = int(winLimits[f - offset][0])
                en = st + int(winLimits[f - offset][1])

                if len(result_list) < en:
                    en = len(result_list)

                result_list = result_list[st:en]

            for result_position in result_list:

                with open(file_key) as f:
                    for i, line in enumerate(f):
                        if i == result_position.string:
                            break
                line = line.strip("\n")

                right_context = line[result_position.start:]
                left_context = line[:result_position.end][::-1]

                for i, token in enumerate(tokenizer.generate_type_AD(left_context)):
                    if i == window_len:
                        break
                start = result_position.end - token.position - len(token.s)

                for i, token in enumerate(tokenizer.generate_type_AD(right_context)):
                    if i == window_len:
                        break
                end = result_position.start + token.position + len(token.s)

                wins.append(TokenWindow(line, [result_position], start, end))

            if len(wins) > 0:
                windows[file_key] = wins
            else:
                windows[file_key] = []

        return self.join_windows(windows)

    def find_window_lim_v2(self, findstr, window_len=3, offset=0, limit=0, winLimits=None):
        """
        Search database and return files
        and positions for the searched word
        witch limits and limits for file transfer in multiple_search 
        """

        if not isinstance(findstr, str):
            raise ValueError
        if not findstr:
            return {}

        windows = {}
        tokenizer = Tokenizer()
        result_dict = self.multiple_search_lim(findstr, offset, limit)

        for f, file_key in enumerate(result_dict.keys()):
            wins = []

            result_list = result_dict[file_key]

            if winLimits is not None:
                st = int(winLimits[f][0])
                en = st + int(winLimits[f][1])

                if st < 0:
                   st = 0

                if len(result_list) < en:
                    en = len(result_list)

            for wi, result_position in enumerate(result_list):

                with open(file_key) as f:
                    for i, line in enumerate(f):
                        if i == result_position.string:
                            break
                line = line.strip("\n")

                right_context = line[result_position.start:]
                left_context = line[:result_position.end][::-1]

                for i, token in enumerate(tokenizer.generate_type_AD(left_context)):
                    if i == window_len:
                        break
                start = result_position.end - token.position - len(token.s)

                for i, token in enumerate(tokenizer.generate_type_AD(right_context)):
                    if i == window_len:
                        break
                end = result_position.start + token.position + len(token.s)

                wins.append(TokenWindow(line, [result_position], start, end))

                wins = self.join_windows({file_key: wins})[file_key]

                if len(wins) == en:
                    break

            if len(wins) > 0:
                windows[file_key] = wins[st:]
            else:
                windows[file_key] = []

        return windows

    def join_windows(self, in_dict):

        window_dict = {}

        for f, wins in in_dict.items():
            pr_win = None
            for win in wins:
                if pr_win is not None and pr_win.window_is_junction(win):
                    for pos in win.positions:
                        if pos not in pr_win.positions:
                            pr_win.positions.append(pos)
                            """
                            he looks at whether the pr_win variable is defined,
                            if yes, then checks whether the windows intersect,
                            if yes then intersects. otherwise, it looks again
                            whether the pr_win variable is defined; if so, it
                            adds it to the window array. pr_win equates to the
                            current window
                            """

                    pr_win.win_start = min(pr_win.win_start, win.win_start)
                    pr_win.win_end = max(pr_win.win_end, win.win_end)
                else:
                    if pr_win is not None:
                        window_dict.setdefault(f, []).append(pr_win)
                    pr_win = win
            if pr_win is not None:
                window_dict.setdefault(f, []).append(pr_win)
            else:
                window_dict.setdefault(f, [])

        return window_dict

    def find_supplemented_window(self, findstr, window_len):

        # Searcher window without limits

        window_dict = self.find_window(findstr, window_len)
        re_right = re.compile(r'[.!?] [A-ZА-Я]')
        re_left = re.compile(r'[A-ZА-Я] [.!?]')

        for f, wins in window_dict.items():
            for win in wins:
                r = win.allString[win.win_end:]
                l = win.allString[:win.win_start + 1][::-1]
                if l:
                    try:
                        win.win_start = win.win_start - re_left.search(l).start()
                    except:
                        win.win_start = 0
                if r:
                    try:
                        win.win_end += re_right.search(r).start() + 1
                    except:
                        win.win_end = len(win.allString)
        return window_dict

    def find_supplemented_window_lim(self, findstr, window_len, offset=0, limit=0, winLimits=None):

        # Searcher window with limits
        window_dict = self.find_window_lim_v2(findstr, window_len, offset, limit, winLimits)

        re_right = re.compile(r'[.!?] [A-ZА-Я]')
        re_left = re.compile(r'[A-ZА-Я] [.!?]')

        for f, wins in window_dict.items():
            for win in wins:
                r = win.allString[win.win_end:]
                l = win.allString[:win.win_start + 1][::-1]
                if l:
                    try:
                        win.win_start = win.win_start - re_left.search(l).start()
                    except:
                        win.win_start = 0
                if r:
                    try:
                        win.win_end += re_right.search(r).start() + 1
                    except:
                        win.win_end = len(win.allString)
        return window_dict
