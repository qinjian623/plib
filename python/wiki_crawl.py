import urllib
from HTMLParser import HTMLParser


def fetch_url(url):
    proxies = {'http': 'http://127.0.0.1:8087'}
    return urllib.urlopen(url, proxies=proxies).read();


class MatchTree():
    def __init__(self, parent_id, node_id):
        self.node_id = node_id;
        self.children = {}
        self.parent = parent_id
        
class Tree():
    def __init__(self):
        self.items = {}
        self.items[0] = TreeItem(0, 0)
    
class TreeItem():
    def __init__(self, ):
        pass
class WikiPageParser(HTMLParser):
    base_info = {}
    in_title = False
    in_content = False
    def handle_starttag(self, tag, attrs):
        if attrs == [('class', 'biTitle')]:
            self.in_title = True
        if attrs == [('class', 'biContent')]:
            self.in_content = True

    def handle_endtag(self, tag):
        if self.in_title:
            self.in_title = False
        if self.in_content:
            self.in_content = False

    def handle_data(self, data):
        if self.in_title:
            self.title = data
        if self.in_content:
            self.base_info[self.title] = data

import xml.etree.ElementTree as ET
from lxml import etree


seed = "https://zh.wikipedia.org/wiki/%E6%B8%85%E5%8D%8E%E5%A4%A7%E5%AD%A6"
seed = "http://baike.baidu.com/view/1563.htm?fr=wordsearch"
seed = "http://baike.baidu.com/view/2914.htm?fr=wordsearch"
data = fetch_url(seed)
tree = etree.HTML(data)

key_path = "body//span[@class='biTitle']"
value_path = "body//div[@class='biContent']"

keys = tree.findall(key_path)
values = tree.findall(value_path)

couples = zip(keys, values)

for (k, v) in couples:
    print k.text, "=",
    for t in v.itertext():
        print t,
    # children = v.getchildren()
    # if children is None or len(children) == 0:
    #     print v.text,
    # else:
    #     if v.text is not None:
    #         print v.text,
    #     for child in children:
    #         print child.text,
    print "\n",
# parser = WikiPageParser()
# parser.feed()
# for key in parser.base_info.keys():
#     print key, parser.base_info[key]
