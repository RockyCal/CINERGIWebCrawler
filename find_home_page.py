__author__ = 'Anoushka'
from tldextract import tldextract

def find_home_page(url):
    ext = tldextract.extract(url)
    ext_dom = ext.domain
    ext_suff = ext.suffix
    new_url = "http://www." + ext_dom + "." + ext_suff
    new_url = new_url.strip('/')
    return new_url
