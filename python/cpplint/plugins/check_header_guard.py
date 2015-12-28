# -*- coding: utf-8 -*-
import re


def register(header_whole, header_line, file_whole, file_line):
    # file_whole.append(check)
    header_whole.append(check)


def header_guard(filename):
    mo = re.search("[^/]*\.h(pp)?$", filename)
    if mo is not None:
        return mo.group(0).replace('.', '_').upper()
    else:
        # TODO throw exception later
        return None


def check(lines, filename, extesion, context):
    guard = header_guard(filename)
    if lines[0] != ('#ifndef %s' % guard):
        context.error_msg(filename, 0, 0,
                          "Header Guard 未定义, 应为: #ifndef %s" % guard)
    if lines[1] != ('#define %s' % guard):
        context.error_msg(filename, 1, 0,
                          "Header Guard 定义错误, 应为: #define %s" % guard)
    if lines[-1] != ('#endif // %s' % guard):
        context.error_msg(filename,
                          len(lines) - 1,
                          0,
                          "Header Guard 格式错误, 应为: #endif // %s" % guard)
