__author__ = 'Anoushka'
from bs4 import BeautifulSoup
from resourceTypes import resourceTypesKnown
import re
from visible import visible
from urllib.request import urlopen


def find_resource_types(url):
    set_of_resources = set()
    souper2 = BeautifulSoup(urlopen(url).read())
    for key in resourceTypesKnown:
        for v in resourceTypesKnown.get(key):
            texts = souper2.find_all(text=re.compile(v))
            visible_texts = filter(visible, texts)
            for vis in visible_texts:
                set_of_resources.add(key)
    resos_found = list(set_of_resources)
    if len(resos_found) > 0:
        return resos_found
    else:
        return ['None']