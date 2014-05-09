#!/usr/bin/python
# -*- coding: utf-8 -*-
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
from BeautifulSoup import BeautifulSoup
import lxml
from lxml import etree
from StringIO import StringIO

wiki_file = "/home/qin/八號坦克鼠式"
wiki_file = "/home/qin/清华大学"
wiki_file = "/home/qin/QF6磅炮"

def str_concat(a, b):
    return a + b

text = reduce(str_concat, open(wiki_file))


parser = etree.HTMLParser()
tree = etree.parse(StringIO(text), parser)

#table = tree.findall("//table[@class='infobox']")

regexpNS = "http://exslt.org/regular-expressions"
table = tree.xpath("//table[@class[re:test(.,'infobox.*')]]",
                   namespaces={'re': regexpNS})

attrs = {}
for row in table[0].findall("tr"):
    th = "".join(row.find("th").itertext()) if row.find("th") is not None else None
    tds = row.findall('td')
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
    print k, '=', v
    attrs[k] = v


# for k, v in attrs.items():
#     print k, '=', v
# parsed_html = BeautifulSoup(text)
# print parsed_html.body.find('table', attrs={'class': 'infobox vcard'}).text

#root = ET.fromstring(text)
#print "".join(root.find("table").itertext())
