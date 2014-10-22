__author__ = 'Anoushka'

from bs4 import BeautifulSoup
from urllib.request import urlopen, Request


def build_title(url):
    req = Request(url)
    page_text = BeautifulSoup(urlopen(req).read())
    title = page_text.find('title', text=True)
    if title is not None:
        if title.has_attr('string'):
            return title.string
        else:
            return title.text
    return 'No title'