# -*- coding: utf-8 -*-
def register(header_whole, header_line, file_whole, file_line):
    file_whole.append(check)
    header_whole.append(check)


def check(lines, filename, extesion, context):
    for idx, line in enumerate(lines):
        if line.find('{') > 0:
            line.lstrip()
