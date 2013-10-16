#!/usr/bin/python3
import json
import sys
import subprocess

class Configuration(object):
    def __init__(self, file_name):
        self._file_name = file_name
        json_obj = self.parser(file_name)
        if not self.checked(json_obj):
            error("config check FAILED, please pay attention to the error-infos above.")
            sys.exit()
        if "global" in json_obj:
            self.global_conf = self.global_configs(json_obj["global"])
        else:
            self.global_conf = self.global_configs(None)
        self.packages_conf = self.packages_configs(json_obj["packages"], self.global_conf)

    def parser(self, file_name):
        json_obj = json.load(open(file_name))
        return json_obj
        
    def global_configs(self, json_obj):
        ret = {
            "mkdir"           :"mkdir",
            "ln"              :"ln -s",
            "cd"              :"cd",
            "rm"              :"rm",
            "lastest_version" : "ls |sort -n |tail - n 1",
            "ssh"             :"ssh",
            "rsync"           :"rsync",
            #meta above
            "version"         :"stable",
            "local_folder"    :"./lib",
            "latest"          :"latest"
            }
        if json_obj is None:
            return ret
        else:
            for k in json_obj.keys():
                ret[k] = json_obj[k]
        return ret

    def merge(self, package, global_):
        for k in global_.keys():
            if k in package:
                continue
            else:
                package[k] = global_[k]
        return package

    def packages_configs(self, json_obj, global_configs):
        ret=[]
        for package in json_obj:
            if global_configs:
                ret.append(self.merge(self.package_configs(package), global_configs))
            else:
                ret.append(self.package_configs(package))
        return ret

    def package_configs(self, json_obj):
        package_values = {
            }
        for k in json_obj.keys():
            package_values[k] = json_obj[k]
        return package_values

    def checked(self, json_obj):
        ret                    = True
        user_in_global_configs = False
        pwd_in_global_configs  = False
        repo_in_global_configs = False
        
        if "global" not in json_obj:
            self.warn("no global configs?")
        else:
            global_configs = json_obj["global"]
            if "user" in global_configs:
                user_in_global_configs = True
            if "password" in global_configs:
                pwd_in_global_configs  = True
            if "host" in global_configs:
                repo_in_global_configs = True

        if "packages" not in json_obj :
            self.error("no packages configs")
            ret = False
        else:
            for package in json_obj["packages"]:
                if "repo" not in package:
                    self.error("package has no repo")
                    ret = False
                if "host" not in package and not repo_in_global_configs:
                    self.error("package repo does NOT exist in global / package configs")
                    ret = False
                if "user" not in package and not user_in_global_configs:
                    self.error("user name does NOT exist in global / package configs")
                    ret = False
        return ret

    def warn(self, msg):
        print ("WARN: "+msg, file=sys.stderr)

    def error(self, msg):
        print ("ERROR: "+msg, file=sys.stderr)


class Engine(object):
    def __init__(self, configuration):
        self._configuration = configuration

    def tune(self, configuration):
        self._configuration = configuration
        
    def start(self):
        for package in self._configuration.packages_conf:
            self.circle(package)
        
    def circle(self, package):
        paras = self.cmd_of_check_version_exists(package)
        paras = self.cmd_of_latest_point(package)
        paras = self.cmd_of_stable_point(package)
        paras = self.cmd_of_download_package(package)
        paras = self.cmd_of_upload_package(package)
        print (paras)
        r = subprocess.call(paras)

    def cmd_of_download_package(self, package):
        paras = ["host", "local_folder", "password", "repo", "rsync", "user","version"]
        ret = ["./download_jar.sh"]
        for para in sorted(paras):
            ret.append(package[para])
        return ret
    
    def cmd_of_check_version_exists(self, package):
        paras = ["host", "mkdir", "password", "repo", "user","version"]
        ret = ["./check_mkdir_exist.sh"]
        for para in sorted(paras):
            ret.append(package[para])
        return ret

    def cmd_of_stable_point(self, package):
        paras = ["host","cd", "ln","password","repo","rm","stable","version","user"]
        ret = ["./stable_point.sh"]
        for para in sorted(paras):
            ret.append(package[para])
        return ret

    def cmd_of_latest_point(self, package):
        paras = ["cd", "host", "latest", "version", "ln", "password", "repo", "rm", "user"]
        ret = ["./latest_point.sh"]
        for para in sorted(paras):
            ret.append(package[para])
        return ret


    def cmd_of_upload_package(self, package):
        paras = ["host", "local_folder", "repo", "rsync","user","version","password"]
        ret = ["./upload_jar.sh"]
        for para in sorted(paras):
            ret.append(package[para])
        return ret

def main():
    conf = Configuration("./config.json")
    e = Engine(conf)
    e.start()
    
if __name__ == '__main__':
    print (json.dumps(main(), sort_keys=True, indent="  "))

