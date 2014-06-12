#!/usr/bin/python
# -*- coding: utf-8 -*-
from wiki_infobox_parser import WikiInfoboxParser
from wiki_infobox_parser import WikiCatlinksParser
from wiki_infobox_parser import WikiTitleParser
from lxml import etree
from os import listdir
import json
import logging

logger = logging.getLogger('mylogger')
logger.info('foorbar')


def log_config():
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler('test.log')
    fh.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    logger.addHandler(fh)
    logger.addHandler(ch)


def str_concat(a, b):
    return a + b


def read_file(file_path):
    return reduce(str_concat, open(file_path))


def parse_html_text_to_tree(html_text):
    return etree.HTML(html_text)


def parse_html_file(html_file):
    return parse_html_text_to_tree(read_file(html_file))


def parse_all_dir(dir_path, parsers):
    wiki_files = listdir(dir_path)
    for wiki_file in wiki_files:
        tree = parse_html_file(dir_path + "/" + wiki_file)
        page = {}
        for k, v in parsers.items():
            page[k] = v.parse(tree)
        print json.dumps(page, sort_keys=True,
                         indent=4, separators=(',', ': '), ensure_ascii=False).encode("utf-8")


parsers = {}
parsers['title'] = WikiTitleParser()
parsers['cats'] = WikiCatlinksParser()
parsers['attrs'] = WikiInfoboxParser()

import sys
parse_all_dir(sys.argv[1], parsers)
