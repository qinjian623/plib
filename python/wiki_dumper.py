#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib2
import thread
import time
import gevent
import Queue
import sys
from urllib2 import quote
#from gevent import monkey
#monkey.patch_all()
done = False


def fetch_url((url, file_path), q):
    #print("Fetching:\t" + url)
    try:
        f = urllib2.urlopen(url)
        data = f.read()
        #print("Writing:\t" + url)
        f = open(file_path, "w")
        f.write(data)
        f.close()
    except:
        print "Unexpected error:", sys.exc_info()[0]
    q.get()
    #print ("Done")


# def fetch_url(url, file_path):
#     print("Fetching:\t" + url)
#     f = urllib2.urlopen(url)
#     data = f.read()
#     print("Writing:\t" + url)
#     f = open(file_path, "w")
#     f.write(data)
#     f.close()
#     print ("Done")


def download_urls(urls):
    jobs = [gevent.spawn(fetch_url, url) for url in urls]
    gevent.joinall(jobs)


def download_thread(queue, number):
    global done

    while not (done and queue.empty()):
        titles = []
        for i in range(number):
            titles.append(queue.get())
        file_paths = [file_path_prefix + title for title in titles]
        urls = [base_url + quote(title) for title in titles]
        para = zip(urls, file_paths)
        download_urls(para)


base_url = "https://zh.wikipedia.org/wiki/"
file_path_prefix = "/home/qin/wiki/"


def q_thread_pool(number, queue):
    total = 0
    global done
    q = Queue.Queue(maxsize=number)
    while not (done and queue.empty()):
        title = queue.get()
        total += 1
        print("Fectching:\t" + title)
        file_path = file_path_prefix + title
        url = base_url + quote(title)
        q.put(thread.start_new_thread(fetch_url, ((url, file_path), q)))
    print ("Total:\t" + str(total))


def read_title_thread(file_path, queue):
    global done
    for line in open(file_path):
        queue.put(line.strip())
    done = True


CURRENT_DOWNLOAD_NUMBER = 1000

q = Queue.Queue(maxsize=1000)

t = thread.start_new_thread(read_title_thread, ("/home/qin/Downloads/zhwiki-latest-all-titles-in-ns0", q))
#thread.start_new_thread(download_thread, (q, 3))
thread.start_new_thread(q_thread_pool, (CURRENT_DOWNLOAD_NUMBER, q))


while not (done and q.empty()):
    time.sleep(10)

print ("DONE")
