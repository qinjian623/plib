#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
from vm import instructiones


def parse_attribute_constant_value(info):
    return int(info, 16)


def parse_attribute_code(info):
    code_attribute = {}
    start = 0
    max_stack = info[start:start+2*2]
    start += 2*2
    code_attribute['max_stack'] = int(max_stack, 16)

    max_locals = info[start:start+2*2]
    start += 2*2
    code_attribute['max_locals'] = int(max_locals, 16)

    code_length = info[start:start+4*2]
    start += 4*2
    code_attribute['code_length'] = int(code_length, 16)
    code = info[start:start+code_attribute['code_length']*2]
    start += code_attribute['code_length']*2
    code_attribute['code'] = code
    code_attribute['decode'] = decompile(code)

    exception_table_length = info[start: start + 2*2]
    code_attribute['exception_table_length'] = int(exception_table_length, 16)
    start += 2*2
    exceptions = []
    for i in range(code_attribute['exception_table_length']):
        exceptions.append(parse_exception(info, start))
        start += 8*2

    attributes_count = info[start: start + 2*2]
    code_attribute['attributes_count'] = int(attributes_count, 16)
    start += 2*2
    attributes, start = parse_attributes(info, code_attribute['attributes_count'], start)
    code_attribute['attributes'] = attributes
    return code_attribute


def parse_attributes(info, count, start):
    attributes = []
    for i in range(count):
        attribute, start = parse_attribute(info, start)
        attributes.append(attribute)
    return attributes, start


def parse_attribute(info, start):
    attribute = {}
    attribute_name_index = info[start:start+2*2]
    attribute['attribute_name_index'] = int(attribute_name_index, 16)
    start += 2*2
    attribute_length = info[start: start + 4*2]
    attribute['attribute_length'] = int(attribute_length, 16)
    start += 4*2
    # TODO 后续的解析
    attribute['info'] = info[start: start + attribute['attribute_length']*2]
    start += attribute['attribute_length']*2
    return attribute, start


def parse_exception(info, start):
    exception = {}
    start_pc = info[start:start+2*2]
    start += 2*2
    exception['start_pc'] = int(start_pc, 16)
    end_pc = info[start:start+2*2]
    start += 2*2
    exception['end_pc'] = int(end_pc, 16)
    handle_pc = info[start:start+2*2]
    start += 2*2
    exception['handle_pc'] = int(handle_pc, 16)
    catch_type = info[start:start+2*2]
    exception['catch_type'] = int(catch_type, 16)


def decompile(code):
    return "\n".join(instructiones(code))


def main():
    print parse_attribute_constant_value("08")

if __name__ == '__main__':
    import sys
    from classloader import parse_classfile
    cls = parse_classfile(sys.argv[1])
    jo = parse_attribute_code(cls['methods'][0]['attributes'][0]['info'])
    print json.dumps(cls['constant_pool'][14]['type'])
    print json.dumps(cls['constant_pool'][1]['type'])
    print json.dumps(jo, sort_keys=True,
                     indent=4, separators=(',', ': '),
                     ensure_ascii=False)# .encode("utf-8")

