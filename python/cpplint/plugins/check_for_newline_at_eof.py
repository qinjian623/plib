# -*- coding: utf-8 -*-
def register(header_whole, header_line, file_whole, file_line):
    file_whole.append(check_whole_file)
    header_whole.append(check_whole_file)


def get_options(options):
    pass


def check_whole_file(lines, filename, extension, options):
    # print filename, "CHECKING"
    if lines[-1]:
        options.error_msg(filename, len(lines) - 1, 0, "文件结尾需要以空行结束")
