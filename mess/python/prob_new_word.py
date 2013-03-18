# -*- coding: utf-8 -*-
#!/bin/python

two_gram_hash_map = {}
two_gram_reverse_hash_map = {}
one_gram_hash_map = {}
prob_hash_map = {}
prev_free_ratio = {}
next_free_ratio = {}


def main(file_string):
    for line in open(file_string):
        #line = line.strip()
        if line[-1] == "\n":
            line = line[0:-1]
        words = line.split(" ")
        for x in range(len(words) - 1):
            put_word_in_one_gram_hash_map(words[x], one_gram_hash_map)
            put_words_in_two_gram_hash_map(words[x], words[x + 1], two_gram_hash_map)
        for x in range(1, len(words)):
            put_words_in_two_gram_hash_map(words[x], words[x - 1], two_gram_reverse_hash_map)
        put_word_in_one_gram_hash_map(words[-1], one_gram_hash_map)
        #put_word_in_one_gram_hash_map(words[-2], one_gram_hash_map)
    cal_free_ratio(one_gram_hash_map, two_gram_hash_map, two_gram_reverse_hash_map, prev_free_ratio, next_free_ratio)
    word_map = cal(one_gram_hash_map, two_gram_hash_map, two_gram_reverse_hash_map, prev_free_ratio, next_free_ratio)
    input()
    for line in open(file_string):
        ranges = []
        if line[-1] == "\n":
            line = line[0:-1]
        words = line.split(" ")[1:-1]
        prev_score = 10000
        pair = []
        pair_is_start = True
        for x in range(len(words) - 1):
            current_score = -100
            if words[x] + " " + words[x + 1] in word_map:
                current_score = word_map[words[x] + " " + words[x + 1]]
            if current_score < 7:
                #abs(prev_score - current_score)/abs(prev_score) > 0.5 and 
                if pair_is_start:
                    pair.append(x)
                else:
                    pair_is_start = True
                pair.append(x + 1)
                ranges.append(pair)
                pair = []
            elif pair_is_start:
                pair.append(x)
                pair_is_start = False
            #print(words[x] + " " + words[x + 1], current_score, prev_score)
            prev_score = current_score
        if len(pair) == 1:
            pair.append(len(words))
            ranges.append(pair)
        print (line[0:-1])
        #print (ranges)
        for p in ranges:
            s = p[0]
            e = p[1]
            print("".join(words[s:e]), end=" ")
        print ("\n", end="")
        input()


def cal_free_ratio(one_gram_hash_map, two_gram_hash_map, two_gram_reverse_hash_map, prev_free_ratio, next_free_ratio):
    for word in one_gram_hash_map.keys():
        prev_free_ratio[word] = free_ratio(word, two_gram_reverse_hash_map)
        next_free_ratio[word] = free_ratio(word, two_gram_hash_map)


def free_ratio(word, two_gram_hash_map):
    import functools
    import math
    r = 0.0
    if word in two_gram_hash_map:
        r = 0.0
        level2_map = two_gram_hash_map[word]
        all_count = functools.reduce(lambda x, y: x + y, level2_map.values())
        for k, v in level2_map.items():
            p = float(v) / float(all_count)
            r += (0 - p * math.log10(p) / math.log10(2))
    return r if r > 0 else 10


def cal(one_gram_hash_map, two_gram_hash_map, two_gram_reverse_hash_map, prev_free_ratio, next_free_ratio):
    ratio_map = {}
    import functools
    import math
    all_count = functools.reduce(lambda x, y: x + y, one_gram_hash_map.values())
    for word, word_count in one_gram_hash_map.items():
        prob_cur = float(word_count) / float(all_count)
        next_map = two_gram_hash_map[word]
        for next, next_count in next_map.items():
            if next_count < 5:
                continue
            prob_next = float(one_gram_hash_map[next]) / float(all_count)
            prob_union = prob_cur * prob_next
            prob_actual = float(next_count) / float(all_count)
            ratio = math.log10(prob_actual / prob_union) / math.log10(2)
            #print (word, next_free_ratio[word], next, prev_free_ratio[next])
            #ratio /= 
            free = min(next_free_ratio[word], prev_free_ratio[next])
            if free < 5:
                ratio_map[word + " " + next] = ratio
    import operator
    x = ratio_map
    #print (ratio_map)
    sorted_x = sorted(x.items(), key=operator.itemgetter(1), reverse=True)
    return x
    for t in sorted_x:
        print (t)
    print(all_count)


def put_words_in_two_gram_hash_map(cur, nxt, two_gram_hash_map):
    if cur in two_gram_hash_map:
        next_map = two_gram_hash_map[cur]
        if nxt in next_map:
            next_map[nxt] += 1
        else:
            next_map[nxt] = 1
    else:
        two_gram_hash_map[cur] = {}
        two_gram_hash_map[cur][nxt] = 1


def put_word_in_one_gram_hash_map(word, one_gram_hash_map):
    if word in one_gram_hash_map:
        one_gram_hash_map[word] += 1
    else:
        one_gram_hash_map[word] = 1

if __name__ == '__main__':
    import sys
    file_string = sys.argv[1]
    main(file_string)
