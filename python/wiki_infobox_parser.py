#!/usr/bin/python
# -*- coding: utf-8 -*-
from lxml import etree
from StringIO import StringIO

wiki_file = "/home/qin/八號坦克鼠式"
#wiki_file = "/home/qin/QF6磅炮"
#wiki_file = "/home/qin/中国地质大学"
wiki_file = "/home/qin/清华大学"


def str_concat(a, b):
    return a + b


def read_file(file_path):
    return reduce(str_concat, open(file_path))


class WikiCatlinksParser():
    def parse(self, tree):
        nodes = tree.xpath("//div[@id='mw-normal-catlinks']")
        if len(nodes) == 0:
            return None
        cats = []
        for node in nodes:
            for a in node.findall("ul/li/a"):
                cat =  "".join(a.itertext())
                cats.append(cat)
        return cats


class WikiTitleParser():
    def parse(self, tree):
        nodes = tree.xpath("//title")
        return "".join(["".join(node.itertext()).split('-')[0].strip()
                        for node in nodes])


class WikiInfoboxParser():
    replace_table = {u'\xa0': ' ',
                     '\n': '::'}

    def parse(self, tree):
        infobox_nodes = tree.xpath("//table[@class[re:test(.,'infobox.*')]]",
                   namespaces={'re': "http://exslt.org/regular-expressions"})
        if len(infobox_nodes) == 0:
            return None
        attrs_of_nodes = []
        for node in infobox_nodes:
            attrs = []
            for row in node.findall("tr"):
                th = "".join(row.find("th").itertext()) if row.find("th") is not None else None
                tds = row.findall("td")
                tdss = ["".join(td.itertext()) for td in tds]

                c = len(tdss)

                k = ""
                v = ""
                if th is None and c == 0:
                    continue

                if th is None:
                    k = tdss[0]
                    if c >= 2:
                        v = "".join(tdss[1:])
                else:
                    k = th
                    v = "".join(tdss)
                v = "".join(map(lambda x: self.replace_table[x] if x in self.replace_table else x, list(v.strip())))
                k = "".join(map(lambda x: self.replace_table[x] if x in self.replace_table else x, list(k.strip())))
                attrs.append((k, v))
            attrs_of_nodes.append(attrs)
        return attrs_of_nodes

#table = tree.findall("//table[@class='infobox']")


# for k, v in attrs.items():
#     print k, '=', v
# parsed_html = BeautifulSoup(text)
# print parsed_html.body.find('table', attrs={'class': 'infobox vcard'}).text

#root = ET.fromstring(text)
#print "".join(root.find("table").itertext())
