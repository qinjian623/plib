# -*- coding: UTF-8 -*-
from pan import RequestCore 
import json

class CloudDownload(object):
    def __init__(self,
                 dst      = "/apps/测试应用/",
                 url      = "/rest/2.0/pcs/services/cloud_dl"):
        self._destination  = dst
        self._url          = url
        
    def download(self, r, src_file):
        ret = {}
        for link in open(src_file):
            var_json = self.add_task(link.strip(), r)
            link = link.strip()
            if "error_code" in var_json:
                print ("Download: Link: "
                       ,link,"Error: ", var_json["error_msg"])
            else:
                ret[int(var_json["task_id"])] = link
                print ("Download: Link: ",link , "Task Id: ", var_json["task_id"])
        return ret

    def add_task(self, r, link):
        params = {
            'save_path'    :self._destination,
            'source_url'   :link,
            'rate_limit'   :50,
            'timeout'      :3600,
            'callback'     :'',
            'method'       :'add_task',
            'access_token' :'3.3be4e87f6e52fbf597c16ab1bfbb37ea.2592000.1382435935.2785319466-248414'
            }
        return r.POST(self._url, params)

    def cancel_task(self, r, task_id):
        params = {
            'method'       :'cancel_task',
            'access_token' :'3.3be4e87f6e52fbf597c16ab1bfbb37ea.2592000.1382435935.2785319466-248414',
            'task_id'      :task_id
            }
        r.POST(self._url, params)

    def list_task(self):
        pass
        
    def query_task(self):
        pass

class CloudDownloadMonitor(object):
    def __init__(self, cycle):
        self._cycle = cycle
        self._tasks = []
        self._messagers = []
    def add_messager(self, messager):
        self._messagers.append（messager）

    def add_monitor_task(self, task_id):
        self._tasks.append(task_id)

    def scan_monitor_tasks(self):
        for task in self._tasks:
            pass
        pass

    def query_task(self, taks_id):
        pass

    def send_message(self, message):
        for messager in self._messagers:
            pass

def main():
    downloader     = CloudDownload()
    request_caller = RequestCore()
    downloader.download(request_caller, "/home/qin/links")

if __name__ == '__main__':
    main()
