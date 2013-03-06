# -*- coding: utf-8 -*-
#!/bin/python

two_gram_hash_map = {}
two_gram_reverse_hash_map = {}
one_gram_hash_map = {}
prob_hash_map = {}


def main(file_string):
    for line in open(file_string):
        line = line.split("null")[1][:-1]
        words = line.split(" ")
        for w in words:
            if w in one_gram_hash_map:
                one_gram_hash_map[w] += 1
            else:
                one_gram_hash_map[w] = 1

        for x in range(len(words) - 2):
            prev = words[x]
            next = words[x + 1]
            if not ((len(prev) == 1 and len(next) > 1) or (len(prev) > 1 and len(next) == 1)):
                continue
            if prev in two_gram_hash_map:
                lel2_map = two_gram_hash_map[prev]
                if next in lel2_map:
                    lel2_map[next] += 1
                else:
                    lel2_map[next] = 1
            else:
                two_gram_hash_map[prev] = {}
                two_gram_hash_map[prev][next] = 1
        for x in range(1, len(words) - 1):
            prev = words[x - 1]
            next = words[x]
            if prev in two_gram_reverse_hash_map:
                lel2_map = two_gram_reverse_hash_map[prev]
                if next in lel2_map:
                    lel2_map[next] += 1
                else:
                    lel2_map[next] = 1
            else:
                two_gram_reverse_hash_map[prev] = {}
                two_gram_reverse_hash_map[prev][next] = 1
    #print (two_gram_hash_map)
    for word, word_count in one_gram_hash_map.items():
        if word_count > 10:
            if word in two_gram_hash_map:
                lel2_map = two_gram_hash_map[word]
                for next_word, two_gram_count in lel2_map.items():
                    if two_gram_count > 10:
                        prob_reverse_two_gram = 1.0
                        if next_word in two_gram_reverse_hash_map:
                            reverse_lel2_map = two_gram_reverse_hash_map[next_word]
                            if word in reverse_lel2_map:
                                ratio = float(reverse_lel2_map[word]) / float(one_gram_hash_map[next_word])
                                prob_reverse_two_gram = ratio
                            else:
                                ratio = 1 / float(one_gram_hash_map[next_word])
                                prob_reverse_two_gram = ratio
                                key = word + "#" + next_word
                                value = float(two_gram_count) / float(word_count)
                                prob_hash_map[key] = value #* prob_reverse_two_gram
            else:
                pass
                #print(word, word_count)

    import operator
    x = prob_hash_map
    sorted_x = sorted(x.items(), key=operator.itemgetter(1), reverse=True)
    for t in sorted_x:
        print (t)

if __name__ == '__main__':
    import sys
    file_string = sys.argv[1]
    main(file_string)
