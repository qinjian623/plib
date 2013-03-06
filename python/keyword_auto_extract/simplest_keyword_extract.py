# -*- coding: utf-8 -*-
#!/bin/python


words_hash_map = {}
new_lines = []
lines = []


def main(file_string):
    all_count = 0
    idnex = 1
    for line in open(file_string):
        len_words = []
        merge_range = []
        line = line.split("null")[0][:-1]
        lines.append(line)
        words = line.split(" ")
        pair = []
        #if idnex >= 52070:
        #    print (idnex, line)
        idnex += 1
        for i in range(len(words)):
            l = len(words[i])
            len_words.append(l)
            if (l == 1) and (i == 0 or len_words[i - 1] != 1):
                pair.append(i)
            if ((l != 1) and len_words[i - 1] == 1) or (i == len(words) - 1 and len_words[i - 1] == 1):
                pair.append(i)
                merge_range.append(pair)
                pair = []
        new_line = []
        for pair in merge_range:
            w = ""
            for c in words[pair[0]:pair[1]]:
                w += c
            new_line.append(w)
            if w in words_hash_map:
                words_hash_map[w] += 1
            else:
                words_hash_map[w] = 1

        for w in words:
            if (len(w) > 1):
                new_line.append(w)
                if w in words_hash_map:
                    words_hash_map[w] += 1
                else:
                    words_hash_map[w] = 1
        new_lines.append(new_line)
    #print_lines()
    print_loc(new_lines, with_loc_tag(new_lines))


def print_lines():
    import functools
    import operator
    all_count = functools.reduce(lambda x, y: x + len(y), new_lines, 0)
    #print (all_count)
    for i in range(len(new_lines)):
        line = new_lines[i]
        print(lines[i])
        t = {}
        for w in line:
            el = e(words_hash_map[w], all_count)
            t[w] = el
        sorted_x = sorted(t.items(), key=operator.itemgetter(1), reverse=True)
        for item in sorted_x:
            print ("\t", item)


def print_loc(new_lines, table):
    import functools
    import operator
    all_count = functools.reduce(lambda x, y: x + len(y), new_lines, 0)
    for line in new_lines:
        t = {}
        print("".join(line))
        if len(line) == 1:
            t[line[0]] = e(table[line[0]]["S"], all_count)
        else:
            t[line[0]] = e(table[line[0]]["B"], all_count)
            t[line[-1]] = e(table[line[-1]]["E"], all_count)
            #print(table[line[-1]], line[-1])
            for w in line[1:-1]:
                t[w] = e(table[w]["I"], all_count)
        sorted_x = sorted(t.items(), key=operator.itemgetter(1), reverse=True)
        for i in sorted_x:
            print ("\t", i)


def with_loc_tag(lines):
    loc_tag_count_table = {}
    for i in range(len(lines)):
        line = new_lines[i]
        length = len(line)
        if length == 1:
            inc_loc_count(line[0], "S", loc_tag_count_table)
        else:
            inc_loc_count(line[0], "B", loc_tag_count_table)
            inc_loc_count(line[-1], "E", loc_tag_count_table)
            for w in line[1:-1]:
                inc_loc_count(w, "I", loc_tag_count_table)
    return loc_tag_count_table


def inc_loc_count(word, loc, table):
    if word in table:
        if loc in table[word]:
            table[word][loc] += 1
        else:
            table[word][loc] = 1
    else:
        table[word] = {}
        table[word][loc] = 1


def e(count, all):
    import math
    return -(math.log10(float(count) / float(all)) / math.log10(2))

if __name__ == '__main__':
    import sys
    file_string = sys.argv[1]
    main(file_string)
