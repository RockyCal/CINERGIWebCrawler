from bs4 import BeautifulSoup
import requests
from openpyxl import Workbook
from openpyxl.compat import range
from openpyxl.cell import get_column_letter

allVisited = []
#Function build_titles prints all the titles of the links on a given site
def build_titles(url):
    asOfVisited = []
    titles = []

    HTTP = 'http://'

    urls = [url]  # stack of urls to scrape
    visited = [url]
    print(url)

    try:
        r = requests.get(url)
    except requests.Timeout:
        print('{}: Timeout error'.format(url))
    except requests.ConnectionError:
        print('{}: Connection error'.format(url))
    except requests.TooManyRedirects:
        print('{}: Too Many Redirects'.format(url))
    except requests.HTTPError:
        print('{}: HTTP Error'.format(url))
    htmlText = r.text
    soup = BeautifulSoup(htmlText)

    for tag in soup.findAll('a', href=True): # filters out the a tag so we can access the right section of HTML
        if HTTP in tag['href']:
            asOfVisited.append(tag)
            visited.append(tag)
            allVisited.append(tag['href'])
    for each in asOfVisited:
        titles.append(each.text)
    return titles

wb = Workbook()

dest_filename = 'Crawl.xlsx'

ws = wb.active

ws.title = "First run"

HTTP = 'http://'
url = "http://www.greenseas.eu/content/standards-and-related-web-information"

urls = [url]  # stack of urls to scrape
visited = [url]  # urls visited

while len(urls) > 0:
    try:
        r = requests.get(urls[0])
        htmlText = r.text
    except requests.Timeout:
        print('{}: Timeout error'.format(url[0]))
    except requests.ConnectionError:
        print('{}: Connection error'.format(url[0]))
    except requests.TooManyRedirects:
        print('{}: Too Many Redirects'.format(url[0]))
    except requests.HTTPError:
        print('{}: HTTP Error'.format(url[0]))

    soup = BeautifulSoup(htmlText)
    urls.pop(0)

for tag in soup.findAll('a', href=True):
        if HTTP in tag['href'] and tag['href'] not in visited:
            urls.append(tag['href'])
            visited.append(tag['href'])

firstRun = build_titles(url)

for col_idx in range(1, 2):
    col = get_column_letter(col_idx)
    for row in range(1, 15):
        ws.cell('%s%s'%(col, row)).value = firstRun[row-1]

log = 1
#Follows the links and crawls the sub-sites
for each in range(1, len(visited)):
    #print(visited[each])
    secondRun = build_titles(visited[each])
    log2 = 0

    for col_idx in range(2, len(secondRun)+1):
        col = get_column_letter(col_idx)
        ws.cell('%s%s'%(col, log)).value = secondRun[log2]
        log2 = log2 + 1

    log = log + 1

#print(visited)
print(allVisited)
print("Length: " + str(len(allVisited)))
wb.save(filename = dest_filename)
