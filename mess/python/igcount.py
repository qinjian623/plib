# -*-  coding:utf-8 -*-
F1='two酒吧.vector'
for line in open(F1):
    items = line.split(' ')
    del items[0]
    for item in items:
        print item.split(':')[0]
