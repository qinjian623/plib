#!/bash/python


def main(file_string):
    wsa = []
    wsb = []
    i = 1
    for line in open(file_string):
        if line == "\n":
            #print(wsa)
            #print(wsb)
            print (i, end="\t")
            compare(wsa, wsb)
            print ("\n", end=" ")
            i += 1
            wsa = []
            wsb = []
        else:
            if len(wsa) == 0:
                wsa = line[0:-1].split(" ")
            else:
                wsb = line[0:-1].split(" ")


def compare(wsa, wsb):
    dc = {}
    for w in wsa:
        if w in dc:
            dc[w] += 1
        else:
            dc[w] = 1
    for w in wsb:
        if w in dc:
            dc[w] += 1
        else:
            dc[w] = 1
    f = 1
    for k, v in dc.items():
        if v == 1:
            print(k, end=" ")
            f = 0

if __name__ == '__main__':
    import sys
    file_string = sys.argv[1]
    print(file_string)
    main(file_string)