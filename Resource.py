__author__ = 'Anoushka'

from check_link import check_link
from crawler_base import brokenLinks
import tldextract
from find_disciplines import find_themes
from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.error import URLError
from urllib.parse import urljoin
from build_title import build_title
from find_resource_types import find_resource_types
from find_organization import find_organization
from find_contact_info import find_contact_info
from find_social_media import find_social_media

class Resource:
    def __init__(self, url):
        link_status = check_link(url)
        if link_status is "working":
            self.link = url
            self.status = link_status
        else:
            if 'www' not in url:
                ext_url = tldextract.extract(url)
                url_sub = ext_url.subdomain
                url_dom = ext_url.domain
                suff = url.split(ext_url.suffix)
                url_suff = ext_url.suffix + suff[1]
                link = "http://www." + url_sub + url_dom + "." + url_suff
                link_status = check_link(link)
                if link_status is "working":
                    self.link = link
                    self.status = link_status
            else:
                brokenLinks.append(url)
                self.link = link_status
                self.status = link_status

    text = ""
    title = "No title"
    status = "No status"
    resource_type = []
    themes = []
    org = "Organization not found"
    resource_contact_person_name = ""
    resource_contact_org = ""
    resource_contact_email = ""
    resource_contact_phone = ""
    url_type = "Type not identified"
    tld = ""
    country_code = ""
    social_media = ""
    links_found = []

    def get_resource_data(self):
        self.title = build_title(self.link)
        self.resource_type = find_resource_types(self.link)
        self.themes = find_themes(self.link)
        self.org = find_organization(self.link)
        find_contact_info(self, self.link)
        # self.url_type = check_type(self.link)
        # self.tld = find_suffix(self.link)
        # self.country_code = find_country_code(self.link)
        self.social_media = find_social_media(self.link)

    def find_links(self):
        if self.status is "working":
            try:
                soup = BeautifulSoup(urlopen(self.link, timeout=7).read())
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
            except URLError as e:
                self.status = "{} {} {}".format(self.link, e.reason)
                brokenLinks.append(self.link)
