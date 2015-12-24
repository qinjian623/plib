# -*- coding: utf-8 -*-
def register(header_whole, header_line, file_whole, file_line):
    file_line.append(check_line)


def check_line(line, line_num, filename, extesion, options):
    rstrip_len = len(line.rstrip())
    space_pos = line.rfind(' ')
    if space_pos >= 0 and space_pos + 1 >= rstrip_len:
        options.error_msg(filename, line_num, space_pos, "行尾请勿保留空格")
