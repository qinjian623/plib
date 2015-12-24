# -*- coding: utf-8 -*-
def register(header_whole, header_line, file_whole, file_line):
    # file_whole.append(check)
    file_line.append(check_line)


def check_line(line, line_num, filename, extesion, options):
    pos = line.find('\t')
    if pos >= 0:
        options.error_msg(filename, line_num, pos, "不要使用TAB, 目前是粗暴检查")
