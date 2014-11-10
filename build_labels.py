__author__ = 'Anoushka'
HTTP = 'http://'

def build_labels(soup):
    titles_found = []
    for tag in soup.find_all('a', href=True):
        if HTTP in tag['href']:
                titles_found.append(tag.text)
                # add to list of total titles
    return titles_found