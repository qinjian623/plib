#!/usr/bin/python

import xml.etree.ElementTree as etree
import random
import MySQLdb
import Queue
import thread
#import xml.sax.saxutils as xmltools

wiki_xml_file = "/home/qin/Desktop/zhwiki-latest-pages-articles.xml"
done = False


def insert(sql):
    try:
        conn = MySQLdb.connect(host="127.0.0.1", user='root',
                               passwd='111qqq,,,',
                               db='my_wiki', port=3306, charset='utf8')
        #print ("Connection estimated...")
        cur = conn.cursor()
        for s in sql:
            #cur.executemany(s)
            cur.execute(s)
        #print ("SQL commiting...")
        conn.commit()
        cur.close()
        conn.close()
        #print ("Connection closed...")
    except MySQLdb.Error as e:
        print ("Mysql Error " + str(e.args[0]) + ": " + str(e.args[1]))


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
                if total % 100 == 0:
                    print ("Total: ", total, )
                    print ("Quere size: ", pages.qsize())
                page = ""
    done = True
    global ts
    ts.get()
    ts.task_done()


def make_auto_increment(start, step):
    l = [0, 1]
    l[0] = start

    def increment():
        l[0] += step
        return l[0]

    def current():
        return l[0]
    return increment, current

inc, current = make_auto_increment(1000000, 1)

tags_we_need = ["id", "ns", "title", "restrictions",
                "redirect title", "revision/id", "revision/model",
                "revision/comment", "revision/contributor/id",
                "revision/contributor/username", "revision/sha1",
                "revision/format", "revision/text"]


page_keys = {"page_id": "id",
             "page_namespace": "ns",
             "page_title": "title",
             "page_restrictions": "restrictions",
             "page_is_redirect":
             lambda x: 0 if x["redirect title"] is None else 1,
             "page_random": lambda x: random.random(),
             "page_latest": "revision/id",
             "page_len": lambda x: len(unicode(x["revision/text"])),
             "page_content_model": "revision/model"}

revision_keys = {"rev_id": "revision/id",
                 "rev_page": "id",
                 "rev_text_id": lambda x: current() + 1,
                 "rev_comment": "revision/comment",
                 "rev_user": "revision/contributor/id",
                 "rev_user_text": "revision/contributor/username",
                 "rev_timestamp": None,
                 "rev_minor_eidt": None,
                 "rev_deleted": None,
                 "rev_len": lambda x: len(unicode(x["revision/text"])),
                 "rev_parent_id": None,
                 "rev_sha1": "revision/sha1",
                 "rev_content_model": "revision/model",
                 "rev_content_format": "revision/format"}

text_keys = {"old_id": lambda x: inc(),
             "old_text": "revision/text",
             "old_flags": lambda x: ""}


def get_value(d, v):
    return d[v]


def funcs_wrapper(v):
    return lambda x: get_value(x, v)


def build_funcs_map(keys_map):
    ret = {}
    for k, v in keys_map.items():

        if isinstance(v, str):
            ret[k] = funcs_wrapper(v)
        elif v is None:
            continue
        else:
            ret[k] = v
    return ret

page_funcs = build_funcs_map(page_keys)
revision_funcs = build_funcs_map(revision_keys)
text_funcs = build_funcs_map(text_keys)


def apply_funcs(funcs, data):
    ret = {}
    for k, f in funcs.items():
        ret[k] = f(data)
    return ret


def produce_text_from_pages(pages, texts):
    global done
    global tags_we_need
    global page_funcs
    global revision_funcs
    global text_funcs

    sql_pages = []
    sql_revisions = []
    sql_texts = []
    while not (done and pages.empty()):
        page = pages.get()
        root = etree.fromstring(page)
        items = [None if item is None else "".join(item.itertext())
                 for item in [root.find(tag) for tag in tags_we_need]]
        d = dict(zip(tags_we_need, items))
        page = apply_funcs(page_funcs, d)
        revision = apply_funcs(revision_funcs, d)
        text = apply_funcs(text_funcs, d)
        sql_pages.append(dict_to_sql(text, "text"))
        sql_revisions.append(dict_to_sql(page, "page"))
        sql_texts.append(dict_to_sql(revision, "revision"))
        if len(sql_pages) > 100:
            insert(sql_pages)
            sql_pages = [] 
        if len(sql_texts) > 100:
            insert(sql_texts)
            sql_texts = []
        if len(sql_revisions) > 100:
            insert(sql_revisions)
            sql_revisions = []

    print ("done")
    global ts
    ts.get()
    ts.task_done()


def dict_to_sql(d, table):
    def escape_string(string):
        return string.replace('\\',
                              '\\\\').replace(
                                  '"',
                                  '\\"').replace("'", "\\'")
    tb_str = "insert into " + table
    tb_col = "(" + ",".join(d.keys()) + ")"
    tb_val_pre = "values ("

    tb_val = ",".join(
        [str(v) if not isinstance(v, basestring) else '"' +
         escape_string(unicode(v)) + '"'
         for v in ["" if v is None else v for v in d.values()]]
    )
    tb_val_suf = ")"
    return tb_str + tb_col + tb_val_pre + tb_val + tb_val_suf


# def wiki_text_to_attr(text):
#     attrs = {}
#     categories = []
#     lines = [xmltools.unescape(line) for line in text.split("\n")]

pages = Queue.Queue(maxsize=10000)

#produce_pages_from_file("/home/qin/Desktop/zhwiki-latest-pages-articles.xml"
#, pages)
thread.start_new_thread(produce_pages_from_file,
                        ("/home/qin/Desktop/zhwiki-latest-pages-articles.xml",
                         pages))

ts = Queue.Queue()
t = thread.start_new_thread(produce_text_from_pages, (pages, None))
ts.put(t)
for i in range(1):
    t = thread.start_new_thread(produce_text_from_pages, (pages, None))
    ts.put(t)


ts.join()

#pages.join()
#print (total)
