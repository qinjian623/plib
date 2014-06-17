#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
@author: Jian QIN
@contact: qinjian@mapbar.com
@version: 0.0.1

1. 命名规范：所有名称都以XXParser命名，其中XX为infobox可以识别出的类型或者识别的目的，不再以Wiki开头。
2. 关系规范：所有Parser都继承统一的一个Parser

@TODO

'''
import json
import re


class Parser():
    """解析器父类，提供通用工具方法和唯一的解析接口"""
    def parse(self, node):
        """
        解析接口

        @param node: xml节点，解析会限制在该节点内容下
        @return: 解析后的结果，可能是{}或者[]
        """
        pass


class TitleParser():
    """Wiki条目名称解析"""
    def parse(self, tree):
        nodes = tree.xpath("//h1[@class['firstHeading']]")
        return "".join(["".join(node.itertext()) for node in nodes])


class CatsParser():
    """用于类型解析"""
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
    """
    别名解析

    实现方法是所有Discription中粗体的词语，单字母的需要跳过，单纯数字的？

    @attention: 本解析器使用范围要限制在DiscriptionParser识别的节点内
    """
    pa = re.compile('[0-9]+')

    def parse(self, node):
        def is_an_alias(x):
            return len(x) > 1 and self.pa.match(x) is None

        json_object = ["".join(b.itertext()) for b in node.xpath('.//b')]
        json_object = filter(is_an_alias, json_object)
        return json_object


class CoodinatesParser():
    """地理坐标解析"""
    coodinates_xpath = [
        './/span[@class="latitude"]',
        './/span[@class="longitude"]'
    ]

    def parse(self, node):
        return ["".join(node.xpath(path_str)[0].itertext())
                for path_str in self.coodinates_xpath]


class DiscriptionParser():
    """描述信息解析"""
    alias_parser = AliasParser()
    coodinates_parser = CoodinatesParser()

    def parse(self, node):
        jo = {}
        ps = node.xpath('.//div[@id="mw-content-text"]/p')
        coodinates = ps[0].xpath('.//span[@id="coordinates"]')
        if len(coodinates) > 0:
            jo['coodinates'] = self.coodinates_parser.parse(coodinates[0])
            discription = ps[1]
        else:
            discription = ps[0]
        jo['alias'] = self.alias_parser.parse(discription)
        jo['text'] = "".join(discription.itertext())
        return jo


class BiotaParser():
    """
    TODO
    biota的特殊处理
    小齒夕鼠屬的动物保护状况案例[特殊的规则来处理]
    """
    pass


class NewUniIBParser():

    def has_jumped_image(self, th, tds):
        # th就是图片
        if th is not None and th.find('.//img') is not None:
            return True
        # 没有th的情况下，td[0]是图片
        if th is None and len(tds) > 0 and\
           tds[0].find('.//img') is not None:
            return True
        # 其他皆不考虑，但是后续需要剔除这个节点
        return False

    def get_title(self, th, tds):
        # 居中、背景色、加粗
        parent_has_background = False
        if th is not None:
            parent = th.getparent()
            if 'style' in parent.attrib:
                parent_has_background = self.is_title_style(
                    parent.attrib['style'])
        elif len(tds) > 0:
            parent = tds[0].getparent()
            if 'style' in parent.attrib:
                parent_has_background = self.is_title_style(
                    parent.attrib['style'])

        th_has_background = th is not None and\
                            'style' in th.attrib and\
                            self.is_title_style(th.attrib['style'])
        if th_has_background or parent_has_background:
            return "".join(th.itertext())

        td_has_background = th is None and len(tds) == 1 and\
                            'style' in tds[0].attrib and\
                            self.is_title_style(
                                tds[0].attrib['style'])
        if td_has_background or parent_has_background:
            return "".join(tds[0].itertext())
        return None

    title_pa = re.compile('background')

    def is_title_style(self, string):
        # IDEA 目前使用的都是背景色的判断，后面要考虑是否会有更严密的判
        # 断
        if NewUniIBParser.title_pa.search(string) is None:
            return False
        else:
            return True

    def remove_small_img(self, tds):
        for td in tds:
            imgs = td.findall('.//img')
            for img in imgs:
                img.getparent().remove(img)

    def parse(self, node):
        json_object = []
        self.parse_wrapped(node, json_object)
        return json_object

    def parse_wrapped(self, node, json_object):
        #TODO 1. logger的加入，方便后续的修正
        #TODO 翡翠2台 依然问题， <external links><br>的替换修改
        previous_row_is_title = False
        previous_row = ""
        for row in node.findall('tr'):
            # 首先还是需要检测出th和td
            th = row.find('th')
            tds = row.findall('td')
            tds_count = len(tds)
            # 跳过图片和跳过行的选择
            if self.has_jumped_image(th, tds):
                continue

            # 递归处理嵌套表格
            if len(row.xpath('.//table')) > 0:
                for table in row.xpath('.//table'):
                    self.parse_wrapped(table, json_object)
                continue
            # 居中、背景色检查
            title = self.get_title(th, tds)
            if title is not None:
                previous_row_is_title = True
                previous_row = title
                continue
            # 普通处理，里面存在img的都要移除节点，外部链接。
            key = ""
            value = ""
            if th is None and tds_count == 0:
                continue
            if previous_row_is_title:
                key = previous_row
                if th is not None and tds_count == 0:
                    value = "".join(th.itertext())
                if th is None and tds_count == 1:
                    value = "".join(tds[0].itertext())
                json_object.append((key, value))
                previous_row_is_title = False
                previous_row = None
                continue

            if th is not None:
                key = "".join(th.itertext())
                # 移除图片节点
                self.remove_small_img(tds)
                value = ",".join(["".join(td.itertext()) for td in tds])
                json_object.append((key, value))
            if th is None and tds_count > 1:
                self.remove_small_img(tds)
                key = "".join(tds[0].itertext())
                value = ",".join(["".join(td.itertext()) for td in tds[1:]])
                json_object.append((key, value))

        return json_object


class UniIBParser():
    # 4. TODO 列表的识别与处理。
    # 6. TODO 翡翠1台这个案例， 问题是折叠隐藏带来的错误。
    # 5. FIX 外部链接 【考虑external text能否过滤出来】。
    # 1. FIX 图片带来的问题, 跳过图片位置是th或者唯一的td的行。
    # 7. FIX 居中、有背景色的，考虑为小标题。[这里利用attrib的属性来一次检
    # 查],style中存在background还有text-align:center的情况 ，其中
    # background是一个强烈信号
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
    p2 = TitleParser()
    p3 = CatsParser()
    p4 = DiscriptionParser()
    p1 = NewUniIBParser()
    for line in open(file_path):
        jo = {}
        tree = parse_html_text_to_tree(line)
        infobox_nodes = tree.xpath(
            "//table[@class[re:test(.,'infobox.*')]]",
            namespaces={'re': "http://exslt.org/regular-expressions"})
        if len(infobox_nodes) == 0:
            continue

        ibs = []
        for infobox in infobox_nodes:
            ibs.append(p1.parse(infobox))
        jo['attrs'] = ibs
        jo['title'] = p2.parse(tree)
        jo['cats'] = p3.parse(tree)
        jo['discripter'] = p4.parse(tree)
        print json.dumps(jo, indent=4,
                         separators=(',', ': '),
                         ensure_ascii=False).encode("utf-8")
        raw_input()


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


def parse_html_text_to_tree(html_text):
    #print len(html_text)
    #return None
    from lxml import etree
    return etree.HTML(html_text)


def parse_html_file(f):
    text = ""
    for line in open(f):
        text += line
    from lxml import etree
    return etree.HTML(text)


def get_title(f):
    p = NewUniIBParser()
    tree = parse_html_file(f)
    infobox_nodes = tree.xpath(
        "//table[@class[re:test(.,'infobox.*')]]",
        namespaces={'re': "http://exslt.org/regular-expressions"})
    for node in infobox_nodes:
        for tr in node.findall('tr'):
            th = tr.find('th')
            tds = tr.findall('td')
            print p.get_title(th, tds)
