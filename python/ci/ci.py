from sh import git
from sh import cd
from sh import make
import sh
import os
import time


class CISettings(object):

    def __init__(self, **args):
        self.db = {"branch": "master"}  # Default settings.
        must_have = ["repo_url",
                     "local_dir",
                     "status_output_dir"]
        for key, val in args.items():
            self.db[key] = val
        self.__check_settings(must_have)

    def __check_settings(self, must_have_settings):
        for i in must_have_settings:
            assert i in self.db

    def __getattr__(self, name):
        if name in self.db:
            return self.db[name]
        super(CISettings, self).__getattribute__(name)


class XimCI(object):

    def __init__(self, settings):
        self.settings = settings
        # Into the context
        if not os.path.exists(self.settings.local_dir):
            git.clone(self.settings.repo_url, self.settings.local_dir)
        cd(settings.local_dir)
        # Make sure checkout the right branch
        git.checkout(settings.branch)
        self.__current_commit = ""

    def loop(self):
        while True:
            # time.sleep(20)
            print "Pulling..."
            git.pull()
            latest_commit = self.__latest_commit()
            if self.__current_commit == latest_commit:
                # Sleep sometime, or next loop
                continue
            self.__current_commit = latest_commit
            try:
                make('test')
            except sh.ErrorReturnCode:
                print "Error"
                continue

    def __latest_commit(self):
        return git.log(-1, pretty="format:%H")


if __name__ == '__main__':
    settings = CISettings(repo_url="https://github.com/qinjian623/dlnotes.git",
                          local_dir="/tmp/ci_test", status_output_dir="iow")
    ci = XimCI(settings)
    ci.loop()
