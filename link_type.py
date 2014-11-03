__author__ = 'Anoushka'
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request


def link_type(url):
    souper2 = BeautifulSoup(urlopen(url).read())
    link_string = ""
    if souper2.find("form") is not None:
        link_string += "search engine"
    if souper2.find(["download" or "programs" or 'software']) is not None:
        link_string += "download"
    if souper2.find("<p>" > "HREF") is not None:
        link_string += "information"
    if souper2.find(["request", "login", "order", "purchase"]) is not None:
        link_string += "offlineAccess"
    return link_string