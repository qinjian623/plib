# -*- coding: utf-8 -*-
def register(header_whole, header_line, file_whole, file_line):
    file_whole.append(check)
    header_whole.append(check)

indent_offset = 8


def get_options(options):
    global indent_offset
    if "check_indent" in options and "indent_offset" in options["check_indent"]:
        indent_offset = options["check_indent"]["indent_offset"]


def check(lines, filename, extension, context):
    for idx, line in enumerate(lines):
        if not speical_cases(lines, idx):
            check_line(line, idx, filename, extension, context)


def speical_cases(lines, idx):
    if idx > 0:
        rstriped_line = lines[idx - 1].rstrip()
        return rstriped_line and rstriped_line[-1] != ';'
    else:
        return False


def check_line(line, line_no, filename, extension, context):
    lead_space_count = len(line) - len(line.lstrip(' '))
    if lead_space_count % indent_offset != 0:
        context.error_msg(filename, line_no, lead_space_count, "Indent数目应该为: "
                          + str(indent_offset))
