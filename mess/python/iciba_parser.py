# -*- coding: utf-8 -*-

from HTMLParser import HTMLParser

def main(filename):
    """
    
    Arguments:
    - `filename`:
    """
    """
    htmlstring = ""
    for line in open(filename):
        htmlstring += line
    """
    import httplib
    conn = httplib.HTTPConnection("www.iciba.com")
    conn.request("GET", "/"+filename)
    r1 = conn.getresponse()
    data1 = r1.read()
    parser = ICiBaParser()
    parser.feed(data1)
    print "\""+ "\",\"".join ([str(parser.groups["popular"]) if "popular" in parser.groups else "0",
      "".join(parser.groups["word"] if "word" in parser.groups else ""),
      " ".join(parser.groups["prop"] if "prop" in parser.groups else ""),
      " ".join(parser.groups["wc"] if "wc" in parser.groups else ""),
      "".join(parser.groups["meaning"] if "meaning" in parser.groups else ""),
      "".join(parser.groups["source"] if "source" in parser.groups else "")]) + "\""
    
class ICiBaParser(HTMLParser):
    __out_format = {
        "common": (lambda data : data),
        "attr_popular": (lambda data : int(data.split(":")[1].split("px")[0])/14)
        }
    __filter_condition = {
        "h1" : [{
            "attr":{"id" : "word_name_h1"},
            "fmt" :"common",
            "group":"word"
            }],
        "strong" : [{
                "attr":{"lang":"EN-US"},
                "fmt":"common",
                "group":"prop"
                },
                    {
                "attr":{},
                "fmt":"common",
                "tag_stack":['html', 'head', 'body', 'div', 'div', 'div', 'div', 'div', 'div', 'p','strong'],
                "group":"wc"
                },
                    {
                "attr":{},
                "fmt":"common",
                "tag_stack":['html', 'head', 'body', 'div', 'div', 'div', 'div', 'div', 'div', 'div', 'p','strong'],
                "group":"wc"
                }
                    ],
        "label" : [{
            "attr":{},
            "fmt":"common",
            "tag_stack":['html', 'head', 'body', 'div', 'div', 'div', 'div', 'div', 'div', 'div', 'p', 'span', 'label'],
            "group":"meaning"
            }],
        "p":[{
            "attr":{},
            "fmt":"common",
            "tag_stack":['html', 'head', 'body', 'div', 'div', 'div', 'div', 'div', 'div', 'div', 'div','ul','li','p'],
            "group":"source"
            }],
        "i":[{
            "attr":{},
            "fmt":"common",
            "tag_stack":['html', 'head', 'body', 'div', 'div', 'div', 'div', 'div', 'div', 'div', 'div','ul','li','p','i'],
            "group":"source"}]
        }

    __attr_rules = {
        "li": [{
                "class":"star_current",
                },
               "style",
               "attr_popular",
               "popular"]
        }

    tag_stack = []
    attr_stack = []
    group_stack=[]

    def __init__(self):
        HTMLParser.__init__(self)
        self.need_p = []
        self.p_format = ""
        self.groups = {}
        self._g = ""


    def data_filter(self, tag, attr):
        ret = False
        if tag not in self.__filter_condition:
            return False
        
        for item in self.__filter_condition[tag]:
            if "tag_stack" in item and self.tag_stack != item["tag_stack"]:
                return False
            if tag=="strong":
                print self.tag_stack
            dic = item["attr"]
            next_loop = False
            for k,v in dic.items():
                if k in attr and attr[k] == v:
                    pass
                else:
                    next_loop = True
                    break
            if next_loop:
                continue
            self.p_format = item["fmt"]
            self._g = item["group"]
            return True
        
        return ret
    
    def attr_filter(self, tag, attr):
        if tag not in self.__attr_rules:
            return
        for k,v in self.__attr_rules[tag][0].items():
            if not(k in attr and attr[k] == v):
                return
        self.groups[self.__attr_rules[tag][3]] = str(self.__out_format[self.__attr_rules[tag][2]](attr[self.__attr_rules[tag][1]]))
        


    def handle_starttag(self, tag, attr):
        self.tag_stack.append(tag)
        self.attr_stack.append(attr)
        tmp_dic={}
        for k,v in attr:
            tmp_dic[k] = v
        p =  self.data_filter(tag, tmp_dic)
        self.need_p.append(p)
        self.group_stack.append(self._g)
        self.attr_filter(tag, tmp_dic)

    def handle_data(self, data):
        if self.need_p and self.need_p[-1]:
            d =  self.__out_format[self.p_format](data)
            if self.group_stack:
                g = self.group_stack[-1]
                if g in self.groups:
                    self.groups[g].append(d) 
                else:
                    self.groups[g] = [d]

    def handle_endtag(self, tag):
        self.need_p.pop()
        self.tag_stack.pop()
        self.attr_stack.pop()
    
if __name__ == '__main__':
    import sys;
    if len(sys.argv) < 2:
        print "./scipt.py html_file_name, thanks."
    main(sys.argv[1])
