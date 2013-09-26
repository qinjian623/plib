# -*- coding: utf-8 -*-
from pan import RequestCore 
import json
import pynotify
import threading
import time

class CloudDownloadAPI(object):
    def __init__(self,
                 request_caller,
                 dst      = "/apps/测试应用/",
                 url      = "/rest/2.0/pcs/services/cloud_dl"):
        self._destination  = dst
        self._url          = url
        self._request_caller = request_caller

    def download(self, src_file):
        """下载src_file中的链接，每行一个链接
        
        Arguments:
        - `self`:
        - `src_file`:下载链接存储文件
        """
        return self._download(self._request_caller, src_file)

    def _download(self, r, src_file):
        ret = {}
        for link in open(src_file):
            link = link.strip()
            var_json = self.add_task(link)
            if "error_code" in var_json:
                print ("Download: Link: "
                       ,link,"Error: ", var_json["error_msg"])
            else:
                ret[int(var_json["task_id"])] = link
        return ret

    def add_task(self, link):
        """增加一个下载任务
        Arguments:
        - `self`:
        - `link`:下载任务的链接
        """
        return self._add_task(self._request_caller, link, self._url)

    def _add_task(self, r, link, url):
        params = {
            'save_path'    :self._destination,
            'source_url'   :link,
            'rate_limit'   :50,
            'timeout'      :3600,
            'callback'     :'',
            'method'       :'add_task',
            'access_token' :'3.3be4e87f6e52fbf597c16ab1bfbb37ea.2592000.1382435935.2785319466-248414'
            }
        return r.POST(url, params)

    def cancel_task(self, task_id):
        """取消一个下载任务
        
        Arguments:
        - `self`:
        - `task_id`:待取消任务的id
        """
        return self.cancel_task(self._request_caller, task_id, self._url)

    def _cancel_task(self, r, task_id, url):
        params = {
            'method'       :'cancel_task',
            'access_token' :'3.3be4e87f6e52fbf597c16ab1bfbb37ea.2592000.1382435935.2785319466-248414',
            'task_id'      :task_id
            }
        r.POST(url, params)

    def list_task(self):
        """获得下载任务列表
        
        Arguments:
        - `self`:
        """
        return self._list_task(self._request_caller, self._url)

    def _list_task(self, r, url):
        params = {
            'method'       :'list_task',
            'access_token' :'3.3be4e87f6e52fbf597c16ab1bfbb37ea.2592000.1382435935.2785319466-248414',
            }
        r.POST(url, params)

    def query_task(self, task_id, op_type = 1):
        """查询指定指定的任务信息
        
        Arguments:
        - `self`:
        - `task_id`:待查询任务的id
        - `op_type`:查询类型，1为查询进度，0为查询信息
        """
        return self._query_task(self._request_caller, task_id, op_type, self._url)

    def _query_task(self, r, task_id, op_type = 1, url=""):
        params = {
            'method'       :'query_task',
            'access_token' :'3.3be4e87f6e52fbf597c16ab1bfbb37ea.2592000.1382435935.2785319466-248414',
            'task_id'      :task_id,
            'op_type'      :op_type
            }            
        return r.POST(url, params)
    def qeury_tasks(self, task_ids, op_type = 1):
        """批量查询任务
        
        Arguments:
        - `self`:
        - `task_ids`:任务列表
        - `op_type`:查询类型，1为查询进度，0为查询信息
        """
        return self._query_tasks(self._request_caller, task_ids, op_type, self._url)

    def _query_tasks(self, r, task_ids, op_type = 1, url = ""):
        params = {
            'method'       :'query_task',
            'access_token' :'3.3be4e87f6e52fbf597c16ab1bfbb37ea.2592000.1382435935.2785319466-248414',
            'task_ids'      :",".join([str(i) for i in task_ids]),
            'op_type'      :op_type
            }
        
        return r.POST(url, params)

class CloudDownloadMonitor(object):
    status = {
        0:'下载成功',
        1:'下载进行中',
        2:'系统错误',
        3:'资源不存在',
        4:'下载超时',
        5:'资源存在但下载失败',
        6:'存储空间不足',
        7:'目标地址数据已存在',
        8:'任务取消'
        }
    
    def __init__(self, cycle, api = None):
        self._api = api
        self._cycle = cycle
        self._tasks = []
        self._tasks_lock = threading.RLock()
        self._messagers = []
        self._tasks_progress_infos = {}
        self._infos_lock = threading.RLock()
        self._monitor_thread = threading.Thread()
        self._stop = threading.Event()
        
    def add_messager(self, messager):
        self._messagers.append(messager)

    def add_monitor_task(self, task_id):
        with self._tasks_lock:
            self._tasks.append(task_id)
    
    def scan_monitor_tasks(self):
        while not self._stop.isSet():
            if self._scan_monitor_tasks(self._api):
                time.sleep(self._cycle)
            else:
                break
        
    def _scan_monitor_tasks(self, api):
        with self._tasks_lock:
            if len(self._tasks) == 0:
                return False
        var_json = api.qeury_tasks(self._tasks)
        if "error_code" in var_json:
            #TODO
            pass
        else:
            with self._infos_lock:
                self._tasks_progress_infos = var_json["task_info"]
        return True

    def start(self):
        self._monitor_thread = threading.Thread(target = self.scan_monitor_tasks).start()
        self._messager_thread = threading.Thread(target = self.scan_tasks_progress_status).start()

    def scan_tasks_progress_status(self):
        while not self._stop.isSet():
            if self._scan_tasks_progress_status():
                time.sleep(self._cycle)
            else:
                break

    def _scan_tasks_progress_status(self):
        with self._infos_lock:
            for key in self._tasks_progress_infos.keys():
                task_info   = self._tasks_progress_infos[key]
                if task_info["result"] == 1:
                    self.send_message("任务ID："+key, "该任务不存在")
                    continue
                status_code = int(task_info["status"])
                file_name   = task_info["file_list"][0]["file_name"]
                source_url  = task_info["source_url"]
                save_path   = task_info["save_path"]
                if status_code != 1:
                    self.send_message("任务ID："+key, "\n来源: "+source_url + "\n存储位置: " + save_path + "\n状态: " + self.status[status_code])
                    with self._tasks_lock:
                        index = self._tasks.index(int(key))
                        del self._tasks[index]
                        if len(self._tasks) == 0:
                            return False
        return True
    
    def stop(self):
        self._stop.set()
    
    def send_message(self, title, message, image = None):
        for messager in self._messagers:
            messager.send(title, message, image)
            
class PynotifyMessager(object):
    def __init__(self, ):
        pass
    def send(self, title, message, image = None):
        if image is None:
            pynotify.init("Pan Message")
            notice = pynotify.Notification(title, message).show()
        else:
            pynotify.init("Pan Message")
            notice = pynotify.Notification(title, message, image).show()
        return notice
        
class TerminalMessager(object):
    def __init__(self, ):
        pass
    def send(self, title, message, image = None):
        print "======================================"
        print "Info: " + title
        print "--------------------------------------"
        print "Message: " + message
        
def main():
    request_caller = RequestCore()
    downloader_api     = CloudDownloadAPI(request_caller)

    tasks = downloader_api.download("/home/qin/links")

    monitor = CloudDownloadMonitor(10, downloader_api)
    monitor.add_messager(PynotifyMessager())
    monitor.add_messager(TerminalMessager())
    for task in tasks.keys():
        monitor.add_monitor_task(task)
    monitor.start()
    monitor.stop()
    
if __name__ == '__main__':
    main()
