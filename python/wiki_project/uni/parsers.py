#!/usr/bin/python
# -*- coding: utf-8 -*-
import json


class WikiCatlinksParser():
    def parse(self, tree):
        nodes = tree.xpath("//div[@id='mw-normal-catlinks']")
        if len(nodes) == 0:
            return None
        cats = []
        for node in nodes:
            for a in node.findall("ul/li/a"):
                cat = "".join(a.itertext())
                cats.append(cat)
        return cats


class AliasParser():
    def parse(self, node):
        json_object = []
        json_object = ["".join(b.itertext()) for b in node.xpath('.//b')]
        return json_object


class DiscriptionParser():
    coodinates_xpath = [
        './/span[@class="latitude"]',
        './/span[@class="longitude"]'
    ]
    alias_parser = AliasParser()

    def parse(self, node):
        jo = {}
        ps = node.xpath('.//div[@id="mw-content-text"]/p')
        coodinates = ps[0].xpath('.//span[@id="coordinates"]')
        if len(coodinates) > 0:
            jo['coodinates'] = ["".join(coodinates[0].
                                        xpath(path_str)[0].itertext())
                                for path_str
                                in DiscriptionParser.coodinates_xpath]
            discription = ps[1]
            jo['text'] = "".join(discription.itertext())
            jo['alias'] = self.alias_parser.parse(discription)
        else:
            discription = ps[0]
            jo['text'] = "".join(discription.itertext())
            jo['alias'] = self.alias_parser.parse(discription)
        return jo


class UniParserTest():
    # TODO 待解决
    # 1. 图片带来的问题。
    # 2. biota问题中的二名法部分。还有异名。【特殊情况】
    # 3. 考虑跳过图片前的所有部分，如果有图片的情况下。【这里要考虑8的
    # 情况】
    # 4. 列表的识别与处理。【】
    # 5. 外部链接 【考虑external text能否过滤出来】。
    # 6. 翡翠1台这个案例， 问题是折叠隐藏带来的错误。
    # 7. 居中、有背景色的，考虑为小标题。[这里利用attrib的属性来一次检
    # 查]
    # 8. 存在th和td的有图片的情况，要特殊处理。【非第一个td的情况下】
    # 9. 小齒夕鼠屬的动物保护状况案例[特殊的规则来处理]
    # DONE 每个页面的第一段中的粗体字具有重要意义，待提出。
    def parse(self, node, json=[]):
        # 以此获取每一行的信息
        # TODO 目前的图片跳过方法有问题
        need_skip_img = False
        if len(node.xpath('.//img')) > 0:
            need_skip_img = True
        for row in node.findall('tr'):

            if need_skip_img:
                print "".join(row.itertext())
                if len(row.xpath('.//img')) > 0:
                    need_skip_img = False
                continue

            # TODO 待修改
            if len(row.xpath('.//img')) > 0:
                continue

            if len(row.xpath('.//table')) > 0:
                for table in row.xpath('.//table'):
                    self.parse(table, json)
                continue

            th = row.find('th')
            tds = row.findall('td')
            tds_count = len(tds)
            # 都没有的情况
            if th is None and tds_count == 0:
                continue

            key = ""
            value = ""
            if th is None:
                key = "".join(tds[0].itertext())
                value = "".join(["".join(td.itertext()) for td in tds[1:]])
            else:
                key = "".join(th.itertext())
                value = "".join(["".join(td.itertext()) for td in tds])
            json.append((key, value))
        return json


def tmp(file_path):
    p2 = WikiTitleParser()
    p3 = WikiCatlinksParser()
    p4 = DiscriptionParser()
    for line in open(file_path):
        jo = {}
        tree = parse_html_text_to_tree(line)
        infobox_nodes = tree.xpath(
            "//table[@class[re:test(.,'infobox.*')]]",
            namespaces={'re': "http://exslt.org/regular-expressions"})
        if len(infobox_nodes) == 0:
            continue
        jo['title'] = p2.parse(tree)
        jo['cats'] = p3.parse(tree)
        jo['discripter'] = p4.parse(tree)
        print json.dumps(jo, indent=4,
                         separators=(',', ': '),
                         ensure_ascii=False).encode("utf-8")
        raw_input()


class WikiTitleParser():
    def parse(self, tree):
        nodes = tree.xpath("//h1[@class['firstHeading']]")
        return "".join(["".join(node.itertext()) for node in nodes])


class WikiInfoboxClassParser():
    def parse(self, tree):
        classes = tree.xpath(
            "//@class[re:test(.,'.*infobox.*')]",
            namespaces={'re': "http://exslt.org/regular-expressions"})
        if len(classes) == 0:
            return None
        t = {}
        for c in classes:
            t[c] = 0
        return ",".join(t.keys())


class WikiInfoboxFootballParser():
    replace_table = {u'\xa0': ' ',
                     '\n': '::'}

    def parse(self, node):
        def replace(a):
            return "".join(map(lambda x: self.replace_table[x]
                               if x in self.replace_table else x,
                               list(a.strip())))
        attrs = []
        for row in node.findall("tr"):
            ## Skip the row without th
            th = "".join(row.find("th").itertext())\
                 if row.find("th") is not None else None
            if th is None:
                continue
            tds = row.findall("td")
            tdss = ["".join(td.itertext()) for td in tds]
            k = th
            v = "".join(tdss)
            v = replace(v)
            k = replace(k)
            if k.encode('utf-8') == '网站':
                v = tds[0].xpath('a/@href')[0]
            attrs.append((k, v))
        return attrs


class WikiInfoboxParserDispatcher():
    replace_table = {u'\xa0': ' ',
                     '\n': '::'}

    def parse(self, tree):
        def replace(a):
            return "".join(map(lambda x: self.replace_table[x]
                               if x in self.replace_table else x,
                               list(a.strip())))

        infobox_nodes = tree.xpath(
            "//table[@class[re:test(.,'infobox.*')]]",
            namespaces={'re': "http://exslt.org/regular-expressions"})
        if len(infobox_nodes) == 0:
            return None
        attrs_of_nodes = []
        for node in infobox_nodes:
            node.xpath('@class')[0]
            attrs = []
            for row in node.findall("tr"):
                th = "".join(row.find("th").itertext())\
                     if row.find("th") is not None else None
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
                v = replace(v)
                k = replace(k)
                attrs.append((k, v))
            attrs_of_nodes.append(attrs)
        return attrs_of_nodes
