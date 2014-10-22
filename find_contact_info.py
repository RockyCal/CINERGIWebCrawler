__author__ = 'Anoushka'
from bs4 import BeautifulSoup
import re
from check_link import check_link
from urllib.request import urlopen


def find_contact_info(reso, url):
    page = BeautifulSoup(urlopen(url).read())
    contact = page.find(text=re.compile('Contact/i'))
    if contact is not None:
        if 'href' in contact:
            if check_link(contact['href']) is "working":
                page = BeautifulSoup(urlopen(contact['href']).read())
    # first look for tag with class = phone
    phone = page.find({'class': 'phone'})
    if phone is not None:
        reso.resource_contact_phone = phone.text
    else:
        # if not class = phone, look for phone number
        phone = page.find(text=re.compile('\+(9[976]\d|8[987530]\d|6[987]\d'
                                          '|5[90]\d|42\d|3[875]\d|2[98654321]'
                                          '\d|9[8543210]|8[6421]|6[6543210]|5'
                                          '[87654321]|4[987654310]|3[9643210]'
                                          '|2[70]|7|1)\d{1,14}$'))
        if phone is not None:
            print(phone)
            reso.resource_contact_phone = phone.text
    email = page.find({'class': 'email'})
    if email is not None:
        reso.resource_contact_email = email.text
    else:
        email = page.find(text=re.compile('\b[A-Z0-9._%+-]+[@(at)][A-Z0-9.-]+\.[A-Z]{2,4}\b'))
        if email is not None:
            reso.resource_contact_email = email.text
