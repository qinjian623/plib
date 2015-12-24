#!/usr/bin/env python
import codecs
from enum import Enum
import importlib
import glob
import os
import sys

# from plugins import


FileExtension = Enum("FileExtension",
                     'C_HEADER CPP_HEADER C_FILE CPP_FILE UNKNOWN')
C_HEADERS_EXTENSION = ['h']
CPP_HEADERS_EXTENSION = ['hpp']
C_FILE_EXTENSION = ['c']
CPP_FILE_EXTENSION = ['cpp', 'cc']


def classify_file_extension(filename):
    extension = filename[filename.rfind('.') + 1:]
    if extension in C_HEADERS_EXTENSION:
        return FileExtension.C_HEADER
    elif extension in CPP_HEADERS_EXTENSION:
        return FileExtension.CPP_HEADER
    elif extension in C_FILE_EXTENSION:
        return FileExtension.C_FILE
    elif extension in CPP_FILE_EXTENSION:
        return FileExtension.CPP_FILE
    else:
        return FileExtension.UNKNOWN


class Options():
    def error_msg(self, filename, line_num, col_num, msg):
        print filename, line_num, col_num, msg


def get_options(opt_file, options):
    pass


def get_filenames():
    pass

whole_header_check_funcs = []
whole_file_check_funcs = []
line_header_check_funcs = []
line_file_check_funcs = []


def whole_header_checks(lines, filename, extension, options):
    for fun in whole_header_check_funcs:
        fun(lines, filename, extension, options)


def whole_file_checks(lines, filename, extension, options):
    for fun in whole_file_check_funcs:
        fun(lines, filename, extension, options)


def line_header_checks(lines, filename, extension, options):
    for line_num,  line in enumerate(lines):
        for fun in line_header_check_funcs:
            fun(line, line_num, filename, extension, options)


def line_file_checks(lines, filename, extension, options):
    for line_num,  line in enumerate(lines):
        for fun in line_file_check_funcs:
            fun(line, line_num, filename, extension, options)


def process_file(filename, options):
    extension = classify_file_extension(filename)
    if extension == FileExtension.UNKNOWN:
        return
    lines = codecs.open(filename, 'r', 'utf8', 'replace').read().split('\n')
    if extension == FileExtension.C_HEADER or extension == FileExtension.CPP_HEADER:
        whole_header_checks(lines, filename, extension, options)
        line_header_checks(lines, filename, extension, options)
    else:
        whole_file_checks(lines, filename, extension, options)
        line_file_checks(lines, filename, extension, options)


FileExtension = Enum("FileExtension",
                     'C_HEADER CPP_HEADER C_FILE CPP_FILE UNKNOWN')


def load_plugins():
    os.chdir("plugins")
    for file in glob.glob("*.py"):
        mod_name = file[:file.rfind('.')]
        if mod_name == "__init__":
            continue
        mod = importlib.import_module("plugins." + mod_name)
        mod.register(
            whole_header_check_funcs,
            line_header_check_funcs,
            whole_file_check_funcs,
            line_file_check_funcs)
    os.chdir("../")


opt_file = ""
options = Options()


def main():
    load_plugins()
    get_options(opt_file, options)
    filenames = sys.argv[1:]
    for filename in filenames:
        process_file(filename, options)

if __name__ == '__main__':
    main()
