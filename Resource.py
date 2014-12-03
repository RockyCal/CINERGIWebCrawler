__author__ = 'Anoushka'

from check_link import check_link
import tldextract
from find_disciplines import find_themes
from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.error import URLError
from urllib.parse import urljoin
from build_title import build_title
from find_resource_types import find_resource_types
from find_organization import find_organization
import re


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
                self.link = link_status
                self.status = link_status

    text = ""
    title = "No title"
    status = "No status"
    resource_type = ""
    themes = ""
    org = "Organization not found"
    resource_contact_person_name = "No contact individual found"
    resource_contact_org = "No contact org"
    resource_contact_email = "No contact email"
    resource_contact_phone = "No contact phone"
    links_found = []

    def get_resource_data(self):
        self.title = build_title(self.link)
        self.resource_type = find_resource_types(self.link)
        self.themes = find_themes(self.link)
        self.org = find_organization(self.link)
        self.find_contact_info()

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

    def get_base(self):
        ext_url = tldextract.extract(self.link)
        base = "http://" + ext_url.subdomain + "." + ext_url.domain + "." + ext_url.suffix
        return base

    def find_contact_info(self):
        page = BeautifulSoup(urlopen(self.link).read())
        contact = page.find('a', text=re.compile('(C|c)ontact.*'))
        if contact is not None:
            if contact.has_attr('href'):
                if check_link(contact['href']) is "working":
                    page = BeautifulSoup(urlopen(contact['href']))
                else:
                    base = self.get_base()
                    link = urljoin(base, contact['href'])
                    if check_link(link) is "working":
                        page = BeautifulSoup(urlopen(link).read())
        # first look for tag with class = phone
        phone = page.find({'class': 'phone'})
        if phone is not None:
            self.resource_contact_phone = phone.text
        else:
            # if not class = phone, look for phone number
            phone = page.find(text=re.compile('\+(9[976]\d|8[987530]\d|6[987]\d'
                                              '|5[90]\d|42\d|3[875]\d|2[98654321]'
                                              '\d|9[8543210]|8[6421]|6[6543210]|5'
                                              '[87654321]|4[987654310]|3[9643210]'
                                              '|2[70]|7|1)\s*(\(\d+\)|\d+)(\s|-)[0-9]+(-*)[0-9]+' ))
            if phone is not None:
                self.resource_contact_phone = phone.strip()
        email = page.find({'class': 'email'})
        if email is not None:
            self.resource_contact_email = email.text
        else:
            email = page.find(text=re.compile('[A-Za-z0-9-._]+(@|\(at\)| at )+[A-Za-z0-9-._]+\.[A-Za-z0-9-._]+'))
            if email is not None:
                self.resource_contact_email = email