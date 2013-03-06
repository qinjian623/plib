#!/bin/python


class Word():
    """docstring for Word"""
    def __init__(self, string, tag, offset):
        super(Word, self).__init__()
        self.string = string
        self.tag = tag
        self.offset = offset

    def to_string(self):
        return self.string + "Tag:" + self.tag + " Offset: " + str(self.offset)


def line_to_words(line):
    r = []
    words = line.split(" ")
    for i in range(len(words)):
        tag = tag_words(i, len(words))
        r.append(Word(words[i], tag, i))
    return r


def tag_words(offset, line_length):
    if line_length == 1:
        return "S"
    if line_length > 5:
        if offset < 3:
            return "B"
        elif offset > line_length - 3:
            return "E"
        else:
            return "I"
    if offset == 0:
        return "B"
    if offset == line_length - 1:
        return "E"
    return "I"


def filter_different_words(pair_lines, unnecessary_words_map):
    delta_words = []
    for l1, l2 in pair_lines:
        words_line1 = l1.split(" ")
        words_line2 = l2.split(" ")
        ws1 = line_to_words(l1)
        ws2 = line_to_words(l2)
        delta1 = [w for w in ws1 if w.string not in words_line2]
        delta2 = [w for w in ws2 if w.string not in words_line1]
        delta_words.append([delta1, delta2])
    for delta1, delta2 in delta_words:
        if len(delta1) != 0 and len(delta2) != 0:
            find_different(delta1, delta2, unnecessary_words_map)


def find_different(delta1, delta2, unnecessary_words_map):
    delta1 = delete_unnecessary_words(delta1, unnecessary_words_map)
    delta2 = delete_unnecessary_words(delta2, unnecessary_words_map)
    #print([w.string for w in delta1])
    #print([w.string for w in delta2])
    new1 = cat_words(delta1)
    new2 = cat_words(delta2)
    for w in new1:
        o = w.offset
        for w2 in new2:
            if o == w2.offset:
                print(w.string, " == ", w2.string)
    #input()


def cat_words(words):
    if len(words) == 0:
        return []
    r = []
    ranges = []
    pair = [0]
    for x in range(1, len(words)):
        if words[x].offset - 1 != words[x - 1].offset:
            pair.append(x)
            ranges.append(pair)
            pair = [x]
        if x == len(words) - 1:
            pair.append(len(words))
            ranges.append(pair)
    if len(ranges) == 0:
        ranges = [[0, 1]]
    for _range in ranges:
        new_word_string = "".join(w.string for w in words[_range[0]:_range[1]])
        new_word_tag = words[_range[0]].tag
        new_word_offset = words[_range[0]].offset
        r.append(Word(new_word_string, new_word_tag, new_word_offset))
    return r


def delete_unnecessary_words(words, unnecessary_words_map):
    r = []
    for x in range(len(words)):
        if words[x].string in unnecessary_words_map:
            count = words[x].string
            if unnecessary_words_map[count] < 10 or len(words[x].string) == 1:  # or (len(words[x].string) == 1 and unnecessary_words_map[count] == 1):
                #print(words[x].string)
                r.append(words[x])
        else:
            r.append(words[x])
    return r


def main(file_string):
    filter_funcs_list = [
    lambda line: line[0: -1] if "\n" in line else line
    ]
    file_list = load_file_to_list(file_string, filter_funcs_list)
    pair_lines = to_pair_lines(file_list)
    delta_words = delta((to_pair_lines(file_list)))
    unnecessary_words = filter_unnecessary_words(delta_words)
    #for w, c in sort_map(count_words(unnecessary_words)):
    #   print(w, c)
    unnecessary_words_map = count_words(unnecessary_words)
    filter_different_words(pair_lines, unnecessary_words_map)


def load_file_to_list(file_string, filter_funcs_list):
    lines = []
    for line in open(file_string):
        for func in filter_funcs_list:
            line = func(line)
        lines.append(line)
    return lines


def to_pair_lines(old_lines):
    lines = []
    pair = []
    for line in old_lines:
        if line == "":
            lines.append(pair[:-1])
            pair = []
            continue
        pair.append(line)
    return lines


def delta(lines):
    delta_words = []
    for line in lines:
        (line1, line2) = line
        words_line1 = line1.split(" ")
        words_line2 = line2.split(" ")
        delta1 = [w for w in words_line1 if w not in words_line2]
        delta2 = [w for w in words_line2 if w not in words_line1]
        delta_words.append([delta1, delta2])
    return delta_words


def filter_unnecessary_words(delta_words):
    l = []
    for words_pair in delta_words:
        (d1, d2) = words_pair
        if len(d1) == 0:
            l.extend(d2)
        elif len(d2) == 0:
            l.extend(d1)
    return l


def count_words(words):
    count_map = {}
    for w in words:
        if w in count_map:
            count_map[w] += 1
        else:
            count_map[w] = 1
    return count_map


def sort_map(t, reverse=False):
    import operator
    return sorted(t.items(), key=operator.itemgetter(1))

if __name__ == '__main__':
    import sys
    file_string = sys.argv[1]
    main(file_string)
