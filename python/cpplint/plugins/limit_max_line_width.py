# -*- coding: utf-8 -*-
def register(header_whole, header_line, file_whole, file_line):
    file_line.append(check)
    header_line.append(check)

max_cols = 80


def get_options(options):
    global max_cols
    if "limit_max_line_width" in options and "max" in options["limit_max_line_width"]:
        max_cols = options["limit_max_line_width"]["max"]


def check(line, line_no, filename, extension, options):
    global max_cols
    if len(line) > max_cols:
        options.error_msg(filename, line_no,  len(line), "超过最大行长度:" + str(max_cols))
