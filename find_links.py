__author__ = 'Anoushka'

import requests
from bs4 import BeautifulSoup
from crawler_base import brokenLinks
from urllib.request import urlopen
from check_link import check_link
from urllib.error import URLError
import tldextract
from urllib.parse import urljoin


def find_links(self):
    if self.status is "working":
        soup = BeautifulSoup(urlopen(self.link).read())
        for link_tag in soup.find_all('a', href=True):
            if check_link(link_tag['href']) is not "working":
                new_url = urljoin(self.link, link_tag['href'])
                if check_link(new_url) is "working" and new_url != self.link:
                    if new_url not in self.links_found:
                        self.links_found.append(new_url)
            else:
                if link_tag['href'] != self.link:
                    if link_tag['href'] not in self.links_found:
                        self.links_found.append(link_tag['href'])