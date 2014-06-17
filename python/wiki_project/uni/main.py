#!/usr/bin/python
# -*- coding: utf-8 -*-

# 1. 读取文件。
# 2. 按照行读取
# 3. 使用不同的解析部件。
# 4. 部件的完善。
#import logging
import json
from lxml import etree
from parsers import CatsParser
from parsers import TitleParser
from parsers import WikiInfoboxClassParser

# logger = logging.getLogger('mylogger')
# def log_config():
#     logger.setLevel(logging.DEBUG)
#     fh = logging.FileHandler('test.log')
#     fh.setLevel(logging.DEBUG)
#     ch = logging.StreamHandler()
#     ch.setLevel(logging.DEBUG)
#     formatter = logging.Formatter(
#         '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
#     fh.setFormatter(formatter)
#     ch.setFormatter(formatter)
#     logger.addHandler(fh)
#     logger.addHandler(ch)


def parse_html_text_to_tree(html_text):
    #print len(html_text)
    #return None
    return etree.HTML(html_text)


def parse_html_file(file):
    text = ""
    for line in open(file):
        text += line
    return etree.HTML(text)


max_line = 100000


def parse_file(file_path, before_hooks, parse_func, after_hooks):
    global max_line
    for line in open(file_path):
        max_line -= 1
        if (max_line < 0):
            break
        html_tree = parse_html_text_to_tree(line)
        for func in before_hooks:
            html_tree = func(html_tree)
        json_object = parse_func(html_tree)
        for func in after_hooks:
            json_object = func(json_object)


def output_json(json_object):
    if (json_object is not None and json_object["class"] is not None):
        for x in json_object["class"].split(","):
            for y in x.split(" "):
                print y.strip()
        print json_object['title'].encode("utf-8")
        # print json.dumps(json_object, sort_keys=True,
        #                  indent=4, separators=(',', ': '),
        #                 ensure_ascii=False).encode("utf-8")


def build_parse_func():
    parsers = {}
    parsers['title'] = TitleParser()
    # parsers['cats'] = WikiCatlinksParser()
    # parsers['attrs'] = WikiInfoboxParser()
    parsers['class'] = WikiInfoboxClassParser()

    def real_func(html_tree):
        if html_tree is None:
            return None
        page = {}
        for k, v in parsers.items():
            page[k] = v.parse(html_tree)

        return page
    return real_func


def main():
    import sys
    file_path = sys.argv[1]
    parse_file(file_path,
               [],
               build_parse_func(),
               [output_json])

if __name__ == '__main__':
    main()
