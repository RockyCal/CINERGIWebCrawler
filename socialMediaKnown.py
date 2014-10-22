__author__ = 'Anoushka'

from bs4 import BeautifulSoup
from check_link import check_link
import requests

social_media_url = 'http://en.wikipedia.org/wiki/List_of_social_networking_websites#L'
socialMediaKnown = []

if check_link(social_media_url) is "working":
    b = requests.get(social_media_url)
    socText = b.text
    soupSoc = BeautifulSoup(socText)

    for tag in soupSoc.find_all('th'):
        socialMediaKnown.append(tag.text)
else:
    print("Error with social media url")
