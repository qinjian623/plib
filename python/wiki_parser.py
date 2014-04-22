import xml.etree.ElementTree as etree

wiki_xml_file = "/home/qin/Desktop/zhwiki-latest-pages-articles.xml"


class CollectorTarget(object):
    output = False

    def start(self, tag, attrib):
        if tag == "{http://www.mediawiki.org/xml/export-0.8/}title":
            self.output = True

    def end(self, tag):
        pass

    def data(self, data):
        if self.output:
            print (data)
            self.output = False


parser = etree.XMLParser(target=CollectorTarget())
#parser.feed(line)


import queue
import _thread as thread
import xml.sax.saxutils as xmltools

class PageParser:
    def __init__(self, file_name, pages):
        self.pages = pages
        self.file_name = file_name

    def work(self):
        to_find_start = True
        for line in open(self.file_name):
            if to_find_start:
                index = line.find("<page>")
                if index == -1:
                    continue
                else:
                    page += index[index:]
                    to_find_start = False
            else:
                index = line.find("</page>")
                if index == -1:
                    page += line
                else:
                    page += line
                    self.pages.put(page)
                    page = ""

done = False


def produce_pages_from_file(file_name, pages):
    total = 0
    to_find_start = True
    page = ""
    global done
    for line in open(file_name):
        if to_find_start:
            index = line.find("<page>")
            if index == -1:
                continue
            else:
                page += line[index:]
                to_find_start = False
        else:
            index = line.find("</page>")
            if index == -1:
                page += line
            else:
                page += line
                pages.put(page)
                total += 1
                #print ("\r\t ", total, end=" ")
                page = ""
    done = True


tags_we_need = ["title", "redirect title", "ns", "revision/text"]


def produce_text_from_pages(pages, texts):
    global done
    global tags_we_need
    total = 0
    c = 0
    while not (done and pages.empty()):
        total += 1
        page = pages.get()
        root = etree.fromstring(page)
        items = [None if item is None else "".join(item.itertext())
                 for item in [root.find(tag) for tag in tags_we_need]]
        wiki_text_to_attr(items[-1])

        c += 1
        if c ==5:
            break


def wiki_text_to_attr(text):
    attrs = {}
    categories = []
    lines = [xmltools.unescape(line) for line in text.split("\n")]
    


pages = queue.Queue(maxsize=10)

#produce_pages_from_file("/home/qin/Desktop/zhwiki-latest-pages-articles.xml"
#, pages)
thread.start_new_thread(produce_pages_from_file,
                        ("/home/qin/Desktop/zhwiki-latest-pages-articles.xml",
                         pages))

thread.start_new_thread(produce_text_from_pages, (pages, None))
#thread.start_new_thread(produce_text_from_pages, (pages, None))
#sleep(1000)
#while not done:


import time
time.sleep(1000)
#pages.join()
#print (total)
