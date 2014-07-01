from bs4 import BeautifulSoup
import requests
from openpyxl import Workbook
from openpyxl.compat import range
from openpyxl.cell import get_column_letter

visitedLinks = []
#Function build_titles prints all the titles of the links on a given site
def build_titles(url):
    """

    @param url: Web page to extract titles from
    @return: List of visited urls

    """
    asOfVisited = []
    titles = []

    HTTP = 'http://'

    urls = [url]  # stack of urls to scrape
    visited = [url]

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

    for tag in soup.findAll('a', href=True): # Finds all tags with links on the page
        if HTTP in tag['href']:
            asOfVisited.append(tag) # visited tags with links
            #print('as of visited: \n{} \nas of visited END.'.format(asOfVisited))
            #visited.append(tag)
            #print('visited: \n{} \n visited END.'.format(asOfVisited))
            visitedLinks.append(tag['href']) # visited links
            #print('allVisited: \n{} \n allVisited END.'.format(allVisited))
    for each in asOfVisited:
        titles.append(each.text)
    return titles
# end build_Titles

# Create excel file
wb = Workbook()
dest_filename = 'Crawl.xlsx'
ws = wb.active
ws.title = "First run"

# Constant for HTTP
HTTP = 'http://'

# start url
start_url = "http://www.greenseas.eu/content/standards-and-related-web-information"

# Block to check functioning of start url
try:
    r = requests.get(start_url)
    htmlText = r.text
except requests.Timeout:
    print('{}: Timeout error'.format(start_url))
except requests.ConnectionError:
    print('{}: Connection error'.format(start_url))
except requests.TooManyRedirects:
    print('{}: Too Many Redirects'.format(start_url))
except requests.HTTPError:
    print('{}: HTTP Error'.format(start_url))

# Make the soup
soup = BeautifulSoup(htmlText)

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
print(visitedLinks)
print("Length: " + str(len(visitedLinks)))
wb.save(filename = dest_filename)
