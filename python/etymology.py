import urllib
from lxml import etree


def get_html_text(url):
    while(True):
        f = urllib.urlopen(url)
        code = f.getcode()
        if code == 200:
            break
    return f.read()


def parse_html_text(text):
    return etree.HTML(text)


def generate_url(word):
    return 'http://dictionary.reference.com/browse/{w}'.format(w=word)


def get_ety(tree):
    ety = tree.find(".//div[@class='ety']")
    if ety is None:
        return ""
    for i in range(2):
        ety.remove(ety.getchildren()[0])
    return "".join(ety.itertext())


def get_info(word):
    tree = parse_html_text(get_html_text(generate_url(word)))
    print get_ety(tree)
