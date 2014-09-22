from urllib.request import urlopen
import urllib.parse
from bs4 import BeautifulSoup
import re

search_name = input("Enter name to search: ")


def visible(element):
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title', 'a']:
        return False
    elif re.match('<!--.*-->', str(element)):
        return False
    return True


def validate_person(name):
    verify_url = "https://orcid.org/orcid-search/quick-search"
    data = {'searchQuery': name}
    url_values = urllib.parse.urlencode(data)
    full_url = verify_url + '?' + url_values
    response = urllib.request.urlopen(full_url)
    soup = BeautifulSoup(urlopen(full_url).read())
    results = soup.find_all(text=re.compile(name))

    if results:
        if visible(results):
            return True
        else:
            return False
    else:
        return False

print(validate_person(search_name))