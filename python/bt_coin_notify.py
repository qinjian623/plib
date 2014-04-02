import pynotify
import sys
import httplib
import sched
import time

RealTimeHUOBI_bt_url = "/staticmarket/td.html"
RealTimeHUOBI_lite_url = "/staticmarket/td_ltc.html"
ReatTimeOKCOIN_bt_url = None
ReatTimeOKCOIN_lite_url = None


## TODO a
class MacNotify():
    def __init__(self):
        pass

    def show(self, title, message):
        pass


class LinuxNotify():
    def __init__(self, name):
        pynotify.init(name)
        self.__notice = None

    def show(self, title, message, update=True):
        if self.__notice is None:
            self.__notice = pynotify.Notification(title, message)
            return self.__notice.show()

        if update:
            self.__notice.update(title, message)
        else:
            self.__notice = pynotify.Notification(title, message)
        return self.__notice.show()

## We don't plan to support any other oses.
system_name_table = {"linux2": lambda x: LinuxNotify(x),
                     "win32":  None,
                     "cygwin": None,
                     "darwin": lambda x: MacNotify(x)}


def createdNotification(name):
    def get_the_system_name():
        return sys.platform
    return system_name_table[get_the_system_name()](name)


class HuobiFetcher():
    def __init__(self):
        self.HUOBI_domain = "market.huobi.com"

    def fetcher(self, url):
        conn = httplib.HTTPConnection(self.HUOBI_domain)
        conn.request("GET", url)
        r1 = conn.getresponse()
        return r1.read().split('\n')


def huobiRealtimeLTC(n, f):
    ltc = f.fetcher(RealTimeHUOBI_lite_url)
    btc = f.fetcher(RealTimeHUOBI_bt_url)
    if ltc[-1].strip() == '' or btc[-1].strip() == '':
        return
    ltc_value = ltc[-1].split(",")[1]
    btc_value = btc[-1].split(",")[1]
    n.show("HUOBI-LTC / HUOBI_BTC",
           ltc_value + "/" + btc_value)


def schedule_loop():
    f = HuobiFetcher()
    n = createdNotification("HuobiInfo")

    while True:
        s = sched.scheduler(time.time, time.sleep)
        s.enter(10, 1, huobiRealtimeLTC, (n, f))
        s.run()

schedule_loop()
