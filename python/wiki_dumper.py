#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib2
import thread
import time
import gevent
import Queue
import sys
import logging
from urllib2 import quote
from os import listdir
#from gevent import monkey
#monkey.patch_all()
done = False

logger = logging.getLogger('mylogger')
logger.info('foorbar')


def log_config():
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler('test.log')
    fh.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    logger.addHandler(fh)
    logger.addHandler(ch)


def fetch_url((url, file_path), (q, title)):
    # try:
    #     raise urllib2.URLError
    # except:
    #     print "Unexpected error:", sys.exc_info()[0], title
    # finally:
    #     q.get()
    try:
        f = urllib2.urlopen(url, timeout=600)
        data = f.read()
        #print("Writing:\t" + url)
        f = open(file_path, "w")
        f.write(data)
        f.close()
        logger.debug("Fetched:\t%s", title)
    except urllib2.URLError as e:
        logger.error("URLError:\t%s\t%s", e.reason, title)
    except:
        logger.error("Unexpected error:\t%s\t%s", sys.exc_info()[0], title)
    finally:
        q.get()


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

        if title in skipped_files:
            logger.debug("SKIPPED:\t%s", title)
            continue
        logger.debug("Fectching:\t%s", title)
        file_path = file_path_prefix + title
        url = base_url + quote(title)
        q.put(thread.start_new_thread(fetch_url,
                                      ((url, file_path),
                                       (q, title))))
    logger.info("Total:\t" + str(total))


def read_title_thread(file_path, queue):
    global done
    for line in open(file_path):
        title = line.strip()
        logger.debug("Adding title:\t" + title)
        queue.put(title)
    done = True


CURRENT_DOWNLOAD_NUMBER = 1000


def exist_files():
    fs = [f.strip() for f in listdir(file_path_prefix)]
    l = range(len(fs))
    return dict(zip(fs, l))


log_config()

q = Queue.Queue(maxsize=1000)
skipped_files = exist_files()

t = thread.start_new_thread(
    read_title_thread,
    ("/home/qin/Downloads/zhwiki-latest-all-titles-in-ns0", q))
#thread.start_new_thread(download_thread, (q, 3))
thread.start_new_thread(q_thread_pool, (CURRENT_DOWNLOAD_NUMBER, q))

while not (done and q.empty()):
    time.sleep(10)
logger.info("ALL DONE")
