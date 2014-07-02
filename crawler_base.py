from bs4 import BeautifulSoup
import requests
from openpyxl import Workbook
from openpyxl.compat import range
from openpyxl.cell import get_column_letter

# Http constant
HTTP = 'http://'

# Make url a global variable if want to go on

def crawl_links(soup):
    # Html tags to investigate
    urls_found = []
    # html_tags = []
    # Add links to url stack
    # Check functioning
    # Add tags
    for tag in soup.find_all('a', href=True):
        if HTTP in tag['href'] and tag['href'] not in visited:
            # check functioning
            check_link(tag['href'])
            # add to list of urls
            urls_found.append(tag['href'])
            # Create list of tags
            # html_tags.append(tag)
    # build_titles(html_tags)
    return urls_found


"""
Name: check_link()
Params: url - link to check
Purpose: Make sure links work and go somewhere
Returns: 1 if link works w/o error
         Exits if link is broken
"""


def check_link(url):
    works = 1
    try:
        link = requests.get(url, timeout=10)
        c = link.status_code
    except requests.Timeout:
        works = 0
        print('{}: Timeout error'.format(url))
        brokenLinks.append(url)
    except requests.ConnectionError:
        works = 0
        print('{}: Connection error'.format(url))
        brokenLinks.append(url)
    except requests.TooManyRedirects:
        works = 0
        print('{}: Too Many Redirects'.format(url))
        brokenLinks.append(url)
    except requests.HTTPError:
        works = 0
        print('{}: HTTP Error'.format(url))
        brokenLinks.append(url)
    else:
        if c != 200:
            works = 0
            print('{}: Error code {}'.format(url, c))
            brokenLinks.append(url)
    return works


"""
Name: build_titles()
Params: url - page to get titles from
Purpose: Extract the title of the pages these links lead to
Returns: List of titles
"""


def build_titles(soup):
    for tag in soup.find_all('a', href=True):
        if HTTP in tag['href'] and tag['href'] not in visited:
            titles.append(tag.text)
    # ######################
    # Use this code if passing in tags
    # Building list of working links
    #for tag in element_tags:
    #    if tag['href'] not in brokenLinks:
    #        titles.append(tag.text)
    return titles


# #####################
# List to hold all broken links
brokenLinks = []
# List of titles - the text attribute of tag
titles = []

# start url
start_url = 'http://www.greenseas.eu/content/standards-and-related-web-information'
start_title = 'GreenSeas Standards and Info'

status = check_link(start_url)  # Check functioning of start url

# Links to visit
urls = []
# visited links
visited = []
tags = []

# Add start url link and title to lists
urls.append(start_url)
visited.append(start_url)
titles.append(start_title)

if status:
    r = requests.get(start_url)
    htmlText = r.text
    soup = BeautifulSoup(htmlText)  # Make the soup
else:
    # exit if start url is broken
    exit()

first_run = crawl_links(soup)
first_titles = build_titles(soup)
second_run = []
second_titles = []
print(first_run)

"""for each in first_run:
    print(each)
    hText = (requests.get(each)).text
    crawlSoup = BeautifulSoup(hText)
    # links found on page
    linksFound = crawl_links(crawlSoup)
    titles_made = build_titles(crawlSoup)
    visited.append(each)
    second_run = second_run + linksFound
    second_titles = second_titles + titles_made
"""
#for url in urls:
#    print(url)
#    hText = (requests.get(url)).text
#    crawlSoup = BeautifulSoup(hText)
#    visited.append(url)
#    urls.pop(0)
#    second_run = crawl_links(crawlSoup)

print('Creating xlsx file')
# Create excel file
wb = Workbook()
filename = 'Crawl.xlsx'
ws = wb.active
ws.title = "First run"

max_first = len(first_run)
for col_idx in range(1, 2):
    col = get_column_letter(col_idx)
    for row in range(1, max_first):
        ws.cell('%s%s' % (col, row)).value = first_titles[row - 1]

# Needs work
i = 0
for row in ws.range('B1:B%s' % (len(first_run) - 1)):
    for cell in row:
        cell.value = first_run[i]
        i += 1

ws1 = wb.create_sheet()
ws1.title = "Second run"
"""
max_second = len(second_run)
for col_idy in range(1, 2):
    col = get_column_letter(col_idy)
    for row in range(1, max_second):
        ws1.cell('%s%s' % (col, row)).value = second_titles[row - 1]

j = 0
for row in ws1.range('B1:B%s' % (len(second_run) - 1)):
    for cell in row:
        cell.value = second_run[j]
        j += 0
"""
"""
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
"""
print('visited: {}'.format(visited))
print('broken links: {}'.format(brokenLinks))
print('titles: {}'.format(titles))
print('Length: ' + str(len(visited)))
wb.save(filename)