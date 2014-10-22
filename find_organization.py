__author__ = 'Anoushka'
from build_title import build_title
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from visible import visible
from urllib.request import urlopen
import urllib.parse
import re

def find_organization(url):
    basic_org = build_title(url)

    # TODO: come up with better way to scrape for org

    return basic_org
    # verify_url = "https://orcid.org/orcid-search/quick-search"
    # data = {'searchQuery': basic_org}
    # url_values = urllib.parse.urlencode(data)
    # full_url = verify_url + '?' + url_values
    # response = urllib.request.urlopen(full_url)
    # soup = BeautifulSoup(urlopen(full_url).read())
    # no_result_text = soup.find(text=re.compile('No results found'))
    # if visible(no_result_text):
    #     return basic_org
    # else:
    #     return "Verified: " + basic_org