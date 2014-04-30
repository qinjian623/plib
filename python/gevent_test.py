import time
import gevent
import thread


def ptime(i, k):
    s = time.time()
    time.sleep(1)
    print (i, time.time() - s)


#gevent.spawn(ptime, i)
#gevent.joinall(jobs)
jobs = [thread.start_new_thread(ptime, (i, i)) for i in range(10)]

time.sleep(5)
