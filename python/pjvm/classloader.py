# -*- coding: utf-8 -*-
import json


def parse_index(bs):
    return int(bs.encode('hex'), 16)


def parse_hex(bs):
    return "".join([format(ord(b), 'x') for b in bs])

constant_type_table = {
    7: 'Class',
    9: 'Fieldref',
    10: 'Methodref',
    11: 'InterfaceMethod',
    8: 'String',
    3: 'Integer',
    4: 'Float',
    5: 'Long',
    6: 'Double',
    12: 'NameAndType',
    1: 'Utf8',
    15: 'MethodHandle',
    16: 'MethodType',
    18: 'InvokeDynamic'
    }

constant_type_parser_functions = {
    7: lambda f, o: parse_constant_class(f, o),
    9: lambda f, o: parse_constant_fmi(f, o),
    10: lambda f, o: parse_constant_fmi(f, o),
    11: lambda f, o: parse_constant_fmi(f, o),
    8: lambda f, o: parse_constant_string(f, o),
    3: lambda f, o: parse_constant_integer(f, o),
    4: lambda f, o: parse_constant_float(f, o),
    5: lambda f, o: parse_constant_long(f, o),
    6: lambda f, o: parse_constant_double(f, o),
    12: lambda f, o: parse_constant_name_and_type(f, o),
    1: lambda f, o: parse_constant_utf8(f, o),
    15: lambda f, o: parse_constant_method_handle(f, o),
    16: lambda f, o: parse_constant_method_type(f, o),
    18: lambda f, o: parse_constant_invoke_dynamic(f, o)
    }


def parse_constant_class(f, o):
    name_index = f.read(2)
    o['name_index'] = parse_index(name_index)


def parse_constant_fmi(f, o):
    class_index = f.read(2)
    o['class_index'] = parse_index(class_index)
    name_and_type_index = f.read(2)
    o['name_and_type_index'] = parse_index(name_and_type_index)


def parse_constant_string(f, o):
    string_index = f.read(2)
    o['string_index'] = parse_index(string_index)


def parse_constant_integer(f, o):
    # TODO 待测试
    value = f.read(4)
    o['value'] = parse_index(value)


def parse_constant_float(f, o):
    # TODO 待测试
    value = f.read(4)
    bits = parse_index(value)
    if bits == 0x7f800000:
        o['value'] = float('+inf')
        return
    if bits == 0xff800000:
        o['value'] = float('-inf')
        return
    if (bits > 0x7f800001 and bits < 0x7fffffff)\
       or (bits > 0xff800001 and bits < 0xffffffff):
        o['value'] = float('nan')
        return

    s = 1 if ((bits >> 31) == 0) else -1
    e = ((bits >> 23) & 0xff)
    m = (bits & 0x7fffff) << 1 if (e == 0) else (bits & 0x7fffff) | 0x800000
    o['value'] = (s*m)*(2**(e-150))


def parse_constant_long(f, o):
    high_bytes = f.read(4)
    low_bytes = f.read(4)
    o['value'] = (high_bytes << 32) + low_bytes


def parse_constant_double(f, o):
    high_bytes = parse_index(f.read(4))
    low_bytes = parse_index(f.read(4))
    bits = (high_bytes << 32) + low_bytes
    if bits == 0x7ff0000000000000L:
        o['value'] = float('-inf')
        return
    if bits == 0xfff0000000000000L:
        o['value'] = float('+inf')
        return
    if (bits > 0x7ff0000000000001L and bits < 0x7fffffffffffffffL) or\
       (bits > 0xfff0000000000001L and bits < 0xffffffffffffffffL):
        o['value'] = float('nan')
        return
    s = 1 if ((bits >> 63) == 0) else -1
    e = ((bits >> 52) & 0x7ffL)
    m = (bits & 0xfffffffffffffL) << 1 if (e == 0) else\
        (bits & 0xfffffffffffffL) | 0x10000000000000L
    o['value'] = (s * m)*(2**(e-1075))


def parse_constant_name_and_type(f, o):
    name_index = f.read(2)
    o['name_index'] = parse_index(name_index)
    descriptor_index = f.read(2)
    o['descriptor_index'] = parse_index(descriptor_index)


def parse_constant_utf8(f, o):
    # TODO 非标准utf-8格式的转化问题
    length = f.read(2)
    o['length'] = parse_index(length)
    bs = f.read(o['length'])
    o['bytes'] = bs


def parse_constant_method_handle(f, o):
    reference_kind = f.read(1)
    reference_index = f.read(2)
    o['reference_kind'] = parse_index(reference_kind)
    o['reference_index'] = parse_index(reference_index)


def parse_constant_method_type(f, o):
    descriptor_index = f.read(2)
    o['descriptor_index'] = parse_index(descriptor_index)


def parse_constant_invoke_dynamic(f, o):
    bootstrap_method_attr_index = f.read(2)
    name_and_type_index = f.read(2)
    o['bootstrap_method_attr_index'] = parse_index(bootstrap_method_attr_index)
    o['name_and_type_index'] = parse_index(name_and_type_index)


def parse_classfile(class_file):
    obj = {}
    cf = open(class_file, 'rb')

    #############
    # Magic部分 #
    #############
    magic = cf.read(4)
    # print "".join([hex(ord(b)) for b in magic])
    obj['magic'] = parse_hex(magic)
    # print obj['magic']

    ###############
    # Version部分 #
    ###############
    minor_version = cf.read(2)
    obj['minor_version'] = parse_index(minor_version)
    major_version = cf.read(2)
    obj['major_version'] = parse_index(major_version)

    ################
    # Constant部分 #
    ################
    constant_pool_count = cf.read(2)
    obj['constant_pool_count'] = parse_index(constant_pool_count)
    # print obj['constant_pool_count']
    pool = parse_constant_pool(cf, obj['constant_pool_count'])
    obj['constant_pool'] = pool
    # print "".join([ord(b) for b in major_version])

    ###################
    # Access flag部分 #
    ###################
    access_flag = cf.read(2)
    obj['access_flag'] = parse_hex(access_flag)
    # print obj['access_flag']

    this_class = cf.read(2)
    super_class = cf.read(2)
    obj['this_class'] = parse_index(this_class)
    obj['super_class'] = parse_index(super_class)
    # print obj['this_class']
    # print obj['super_class']

    #################
    # Interface部分 #
    #################
    interfaces_count = cf.read(2)
    obj['interfaces_count'] = parse_index(interfaces_count)
    obj['interfaces'] = parse_interfaces(cf, obj['interfaces_count'])

    ##############
    # Fields部分 #
    ##############
    fields_count = cf.read(2)
    obj['fields_count'] = parse_index(fields_count)
    obj['fields'] = parse_fields(cf, obj['fields_count'])
    # print obj['fields_count']

    ##############
    # Method部分 #
    ##############
    methods_count = cf.read(2)
    obj['methods_count'] = parse_index(methods_count)
    obj['methods'] = parse_methods(cf, obj['methods_count'])
    # print obj['methods_count']

    ##################
    # Attributes部分 #
    ##################
    attributes_count = cf.read(2)
    obj['attributes_count'] = parse_index(attributes_count)
    obj['attributes'] = parse_attributes(cf, obj['attributes_count'])
    # print obj['attributes_count']
    print json.dumps(obj, sort_keys=True,
                     indent=4, separators=(',', ': '),
                     ensure_ascii=False)# .encode("utf-8")
    return obj


def parse_methods(cf, count):
    methods = []
    for i in range(count):
        methods.append(parse_method(cf))
    return methods


def parse_method(f):
    method_info = {}
    access_flags = f.read(2)
    name_index = f.read(2)
    descriptor_index = f.read(2)
    attributes_count = f.read(2)
    method_info['access_flags'] = parse_hex(access_flags)
    method_info['name_index'] = parse_index(name_index)
    method_info['descriptor_index'] = parse_index(descriptor_index)
    method_info['attributes_count'] = parse_index(attributes_count)
    method_info['attributes'] = parse_attributes(
        f,
        method_info['attributes_count'])
    return method_info


def parse_fields(cf, count):
    fields = []
    for i in range(count):
        fields.append(parse_field(cf))
    return fields


def parse_field(f):
    field = {}
    access_flags = f.read(2)
    name_index = f.read(2)
    descriptor_index = f.read(2)
    attributes_count = f.read(2)

    field['access_flags'] = parse_hex(access_flags)
    field['name_index'] = parse_index(name_index)
    field['descriptor_index'] = parse_index(descriptor_index)
    field['attributes_count'] = parse_index(attributes_count)
    field['attributes'] = parse_attributes(f, field['attributes_count'])
    return field


def parse_attributes(f, count):
    attributes = []
    for i in range(count):
        attributes.append(parse_attribute(f))
    return attributes


def parse_attribute(f):
    attribute = {}
    attribute_name_index = f.read(2)
    attribute['attribute_name_index'] = parse_index(attribute_name_index)
    attribute_length = f.read(4)
    attribute['attribute_length'] = parse_index(attribute_length)
    # TODO 需要根据具体类型进行分析
    attribute['info'] = parse_hex(f.read(attribute['attribute_length']))
    return attribute


def parse_interfaces(cf, count):
    interfaces = []
    for i in range(count):
        interface_index = parse_interface(cf)
        interfaces.append(interface_index)
    return interfaces


def parse_interface(cf):
    interface_index = cf.read(2)
    return parse_index(interface_index)


def parse_constant_pool(cf, count):
    pool = []
    pool.append(None)

    i = 1
    while (i < count):
        cp_info = parse_constant(cf)
        cp_info['type'] = constant_type_table[cp_info['tag']]
        pool.append(cp_info)
        if cp_info['tag'] == 5 or cp_info['tag'] == 6:
            pool.append(None)
            i += 1
        i += 1
    return pool


def parse_constant(cf):
    cp_info = {}
    tag = cf.read(1)
    cp_info['tag'] = int(tag.encode('hex'), 16)
    parse_func = constant_type_parser_functions[cp_info['tag']]
    parse_func(cf, cp_info)
    return cp_info


if __name__ == '__main__':
    import sys
    cls = parse_classfile(sys.argv[1])
    # while(True):
    #     no = raw_input()
    #     print json.dumps(
    #         cls['constant_pool'][int(no)], sort_keys=True,
    #         indent=4, separators=(',', ': '),
    #         ensure_ascii=False).encode("utf-8")
