#!/usr/bin/env python
# -*- coding: utf-8 -*-
import codecs
from enum import Enum
import importlib
import glob
import os
import sys
import json
import sre_compile

# from plugins import


FileExtension = Enum("FileExtension",
                     'C_HEADER CPP_HEADER C_FILE CPP_FILE UNKNOWN')
C_HEADERS_EXTENSION = ['h']
CPP_HEADERS_EXTENSION = ['hpp']
C_FILE_EXTENSION = ['c']
CPP_FILE_EXTENSION = ['cpp', 'cc']
_regexp_compile_cache = {}


def match(pattern, s):
    """Matches the string with the pattern, caching the compiled regexp."""
    # The regexp compilation caching is inlined in both Match and Search for
    # performance reasons; factoring it out into a separate function turns out
    # to be noticeably expensive.
    if pattern not in _regexp_compile_cache:
        _regexp_compile_cache[pattern] = sre_compile.compile(pattern)
    return _regexp_compile_cache[pattern].match(s)


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


class Context():
    def __init__(self):
        pass

    def error_msg(self, filename, line_num, col_num, msg):
        print filename + ":" + str(line_num), col_num, msg

    def set_options(self, options):
        self._options = options

    def options(self):
        return self._options


def load_options(opt_file):
    return json.load(open(opt_file))


whole_header_check_funcs = []
whole_file_check_funcs = []
line_header_check_funcs = []
line_file_check_funcs = []


def whole_header_checks(lines, filename, extension, context):
    for fun in whole_header_check_funcs:
        fun(lines, filename, extension, context)


def whole_file_checks(lines, filename, extension, context):
    for fun in whole_file_check_funcs:
        fun(lines, filename, extension, context)


def line_header_checks(lines, filename, extension, context):
    for line_num,  line in enumerate(lines):
        for fun in line_header_check_funcs:
            fun(line, line_num, filename, extension, context)


def line_file_checks(lines, filename, extension, context):
    for line_num,  line in enumerate(lines):
        for fun in line_file_check_funcs:
            fun(line, line_num, filename, extension, context)


def process_file(filename, context):
    extension = classify_file_extension(filename)
    if extension == FileExtension.UNKNOWN:
        return
    lines = codecs.open(filename, 'r', 'utf8', 'replace').read().split('\n')
    if extension == FileExtension.C_HEADER or extension == FileExtension.CPP_HEADER:
        whole_header_checks(lines, filename, extension, context)
        line_header_checks(lines, filename, extension, context)
    else:
        whole_file_checks(lines, filename, extension, context)
        line_file_checks(lines, filename, extension, context)


FileExtension = Enum("FileExtension",
                     'C_HEADER CPP_HEADER C_FILE CPP_FILE UNKNOWN')


def load_plugins():
    # load the plugins
    os.chdir("plugins")
    for file in glob.glob("*.py"):
        mod_name = file[:file.rfind('.')]
        mod = importlib.import_module("plugins." + mod_name)
        if "get_options" in dir(mod):
            mod.get_options(context.options())
        if "register" in dir(mod):
            mod.register(
                whole_header_check_funcs,
                line_header_check_funcs,
                whole_file_check_funcs,
                line_file_check_funcs)
    # back to original path
    os.chdir("../")


context = Context()


def main():
    opt_file = sys.argv[1]
    context.set_options(load_options(opt_file))
    load_plugins()
    filenames = sys.argv[2:]
    for filename in filenames:
        process_file(filename, context)

if __name__ == '__main__':
    main()
