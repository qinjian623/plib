#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib
import gevent
from urllib import quote
import time


def fetch_url(url):
    s = time.time()
    #p = {'http': 'http://127.0.0.1:8087'}
    data = urllib.urlopen(url).read()
    print (time.time() - s)
    return data


base_url = "https://zh.wikipedia.org/wiki/"
#base_url = "http://www.baidu.com/"
THREADS_NUMBER = 4

titles = ["清华大学", "北京理工大学", "北京邮电大学", "北京交通大学", "北京科技大学"]
urls = [base_url + quote(title) for title in titles]
print (urls)
jobs = [gevent.spawn(fetch_url, url) for url in urls]
print ("gevent.spawn DONE")
gevent.joinall(jobs)
# for title in titles:
#     data = fetch_url(base_url + title)
#     print (title + " finished.")
print ("DONE")
