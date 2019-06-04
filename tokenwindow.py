from searchengine import SearchEngine


def main():

    win = SearchEngine('database')
    while True:
        findstr = input("Слово для поиска: ")
        if findstr == "exit":
            break

        res = win.find_supplemented_window(findstr, 2)#2 - deth of window
        for k in res: #k - key
            print(k)
            for v in res[k]:
                print(v) #v- meaning from the list
                print (v.get_BB_string())

if __name__ == "__main__":
    main()
"""
the window is the dictionary, where a key is a file name,
and the meaning is a list of windows
"""
