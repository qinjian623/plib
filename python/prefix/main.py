#!/usr/bin/env python
one_gram = {}
# current then, prefix
two_gram = {}


def main(file_path):
    for line in open(file_path):
        words = line.split(' ')
        one_gram_counted = set()
        words_c = len(words)
        for word in words:
            if word not in one_gram_counted and word in one_gram:
                one_gram[word] = one_gram[word] + 1
                one_gram_counted.add(word)
            elif word not in one_gram_counted:
                one_gram[word] = 1
                one_gram_counted.add(word)
        for prefix, current in zip(range(0, words_c-1), range(1, words_c)):
            pre = words[prefix]
            cur = words[current]
            if cur in two_gram:
                if pre in two_gram[cur]:
                    two_gram[cur][pre] += 1
            else:
                two_gram[cur] = {}
                two_gram[cur][pre] = 1
    ratio = {}
    for word, wc in one_gram.items():
        if word not in two_gram:
            continue
        for prefix, pwc in two_gram[word].items():
            ratio[prefix + word] = wc/pwc

    for pair, wc in ratio.items():
        print(str(wc) + " " + pair)

if __name__ == '__main__':
    import sys
    main(sys.argv[1])
