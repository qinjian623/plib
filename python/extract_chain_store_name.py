#!/usr/bin/env python


def main(file="/home/qin/Desktop/chain"):
    words_count = {}
    words_company = {}
    poi_count = 0
    for line in open(file):
        poi_count += 1
        words = line.strip().split(" ")
        for word in words:
            if word not in words_count:
                words_count[word] = 1
            else:
                words_count[word] = words_count[word] + 1
            if word in words_company:
                words_company[word] = words_company[word] | set(words)
            else:
                words_company[word] = set(words)

    ten_percent_count = poi_count * 0.1
    for word in words_count.keys():
        this_word_count = words_count[word]
        # if (len(word.decode('utf-8')) == 1):
        #     continue
        if this_word_count > 1000:
            continue
        if (this_word_count < 3 or this_word_count > ten_percent_count):
            continue
        print len(words_company[word])/float(words_count[word]), word, len(words_company[word]), words_count[word]
        # print

if __name__ == '__main__':
    main()
