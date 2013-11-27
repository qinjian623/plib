import sys
import os
import operator
import pri

def prob_scale(file_path):
    scores      = [float(line.split(",")[0]) for line in open(file_path)]
    names       = [line.strip().split(",")[1] for line in open(file_path)]
    min_score   = min(scores)
    score_range = max(scores) - min_score
    ret         = dict(zip(names, [(score - min_score)/ score_range for score in scores]))
    ret[None]   = 0
    return ret

def prob(base, words, pri):
    ret = {}
    for tp in base.keys():
        type_base = base[tp]
        prob = 1
        for word in words:
            if word in type_base:
                prob = prob * type_base[word]
            else:
                prob = prob * type_base[None]
        # if tp in pri:
        #     prob *= pri[tp]
        # else:
        #     prob *= 0
                
        ret[tp] = prob
    return sorted(ret.items(), key=operator.itemgetter(1), reverse= True)

if __name__ == '__main__':
    directory = sys.argv[1]
    pri_file = sys.argv[2]
    base = {}
    pri_base = pri.pri(pri_file)
    for f in os.listdir(directory):
        base[f.split(".")[0]]  = prob_scale(os.path.join(directory, f))

    while True:
        words = input().split(" ")
        print (words)
        for t in prob(base, words, pri_base)[0:10]:
            print (t)
        



