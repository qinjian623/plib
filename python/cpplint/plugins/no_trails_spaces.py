# -*- coding: utf-8 -*-
def register(header_whole, header_line, file_whole, file_line):
    # file_line.append(check_line)
    file_whole.append(check_whole_file)
    # header_line.append(check_line)
    header_whole.append(check_whole_file)


def get_opionts(options):
    print options["ok"]


def check_whole_file(lines, filename, extension, options):
    for idx, line in enumerate(lines):
        check_line(line, idx, filename, extension, options)


def check_line(line, line_num, filename, extension, options):
    rstrip_len = len(line.rstrip())
    space_pos = line.rfind(' ')
    if space_pos >= 0 and space_pos + 1 >= rstrip_len:
        options.error_msg(filename, line_num, space_pos, "行尾请勿保留空格")
