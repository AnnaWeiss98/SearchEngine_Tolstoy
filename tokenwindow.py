from searchengine import SearchEngine


def main():

    win = SearchEngine('database')
    while True:
        findstr = input("Слово для поиска: ")
        if findstr == "exit":
            break

        res = win.find_window(findstr, 2)
        for k in res:
            print(k) # k - keys
            for v in res[k]:
                print(v) # v - value from list

if __name__ == "__main__":
    main()
