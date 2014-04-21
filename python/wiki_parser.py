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
            
parser = etree.XMLParser(target = CollectorTarget())
#parser.feed(line)

import queue
import _thread as thread
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
                    page += index[index :]
                    to_find_start = False
            else:
                index = line.find("</page>")
                if index == -1:
                    page += line
                else:
                    page += line
                    self.pages.put(page)
                    page = ""

def produce_pages_from_file(file_name, pages):
    to_find_start = True
    for line in open(file_name):
        if to_find_start:
            index = line.find("<page>")
            if index == -1:
                continue
            else:
                page += index[index :]
                to_find_start = False
        else:
            index = line.find("</page>")
            if index == -1:
                page += line
            else:
                page += line
                pages.put(page)
                page = ""

total = 0
def produce_text_from_pages(pages, texts):
    page = pages.get()
    sleep(1000)
    total += 1
    pages.task_done()
    

pages = queue.Queue()
thread.start_new_thread(produce_pages_from_file, ("/home/qin/Desktop/zhwiki-latest-pages-articles.xml",pages))

thread.start_new_thread(produce_text_from_pages, (pages, None))
thread.start_new_thread(produce_text_from_pages, (pages, None))
pages.join()
print (total)

    

    
