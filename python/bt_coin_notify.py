import pynotify
import sys
import httplib

RealTimeHUOBI_bt_url = "/staticmarket/td.html"
RealTimeHUOBI_lite_url = "/staticmarket/td_ltc.html"
ReatTimeOKCOIN_bt_url = None
ReatTimeOKCOIN_lite_url = None


def notify_linux(title, message):
    pynotify.init("Basic")
    notice = pynotify.Notification(
        title,
        message
    ).show()
    return notice


## TODO Will use the apple script
def notify_mac(title, message):
    pass


## TODO
def notify_win32(title, message):
    pass

## We don't plan to support any other oses.
system_name_table = {"linux2": notify_linux,
                     "win32":  notify_win32,
                     "cygwin": None,
                     "darwin": notify_mac}


def get_the_system_name():
    return sys.platform


def send_notification(title, message):
    f = system_name_table[get_the_system_name()]
    if f is None:
        return False
    f(title, message)
    return True


class HuobiFetcher():
    def __init__(self):
        self.HUOBI_domain = "market.huobi.com"

    def fetcher(self, url):
        conn = httplib.HTTPConnection(self.HUOBI_domain)
        conn.request("GET", url)
        r1 = conn.getresponse()
        return r1.read().split('\n')


f = HuobiFetcher()
ltc = f.fetcher(RealTimeHUOBI_lite_url)
btc = f.fetcher(RealTimeHUOBI_bt_url)

send_notification(ltc[1] + "/" + btc[1],
                  ltc[2] + "/" + btc[2])
