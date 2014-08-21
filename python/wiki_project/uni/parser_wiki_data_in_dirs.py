#!/usr/bin/env python
import os
import json
from main import parse_html_text_to_tree
from parsers import CatsParser
from parsers import TitleParser
from parsers import DiscriptionParser
from parsers import NewUniIBParser


def process_file(dir, call_back):
    for file_name in os.listdir(dir):
        call_back("".join([i.rstrip('\n') for i in open(dir + "/" + file_name)]))


def list_dir(root_dir, call_back):
    for dir_ in os.listdir(root_dir):
        print >> sys.stderr, dir_
        process_file(root_dir + "/" + dir_, call_back)


read = {}
p2 = TitleParser()
p3 = CatsParser()
p4 = DiscriptionParser()
p1 = NewUniIBParser()


def parse_func(tree):
    jo = {}
    if tree is None:
        return
    title = p2.parse(tree)
    if title in read:
        return
    print >> sys.stderr, title
    jo['title'] = title
    jo['cats'] = p3.parse(tree)
    jo['discripter'] = p4.parse(tree)
    ibs = []

    infobox_nodes = tree.xpath(
        "//table[@class[re:test(.,'infobox.*')]]",
        namespaces={'re': "http://exslt.org/regular-expressions"})
    if len(infobox_nodes) != 0:
        for infobox in infobox_nodes:
            ibs.append(p1.parse(infobox))
    jo['attrs'] = ibs
    print json.dumps(jo, indent=4,
                     separators=(',', ': '),
                     ensure_ascii=False).encode("utf-8")
    # parsers = {}
    # parsers['title'] = TitleParser()
    # parsers['cats'] = WikiCatlinksParser()
    # parsers['attrs'] = WikiInfoboxParser()
    # # parsers['class'] = WikiInfoboxClassParser()
    # if html_tree is None:
    #     return None
    # page = {}
    # for k, v in parsers.items():
    #     page[k] = v.parse(html_tree)
    # return page


def hook_func(msg):
    html_tree = parse_html_text_to_tree(msg)
    parse_func(html_tree)

if __name__ == '__main__':
    import sys
    list_dir(sys.argv[1], hook_func)
