from bs4 import BeautifulSoup
import requests
from openpyxl import Workbook, cell
from openpyxl.cell import coordinate_from_string

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
            visited.append(tag['href'])
            # check functioning, will add to brokenLinks if link is bad
            check_link(tag['href'])
            # add to list of urls found
            if tag['href'] not in brokenLinks:
                # add to list of working urls found to be written
                urls_found.append(tag['href'])
                # add to global list of working urls
                urls.append(tag['href'])
            # Create list of tags
            # html_tags.append(tag)
            # mark as visited
            # visited.append(tag['href'])
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
    except:
        works = 0
        print('{}: Unexpected Error'.format(url))
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
    titles_found = []
    for tag in soup.find_all('a', href=True):
        if HTTP in tag['href']:
            if tag['href'] not in brokenLinks:
                titles_found.append(tag.text)
                # add to list of total titles
                titles.append(tag.text)
    # ######################
    # Use this code if passing in tags
    # Building list of working links
    #for tag in element_tags:
    #    if tag['href'] not in brokenLinks:
    #        titles.append(tag.text)
    return titles_found


# #####################
# Total visited links
visited = []
# Total working links found
urls = []
# Total broken links
brokenLinks = []
# Total titles - the text attribute of tag
titles = []

# start url
start_url = 'http://www.greenseas.eu/content/standards-and-related-web-information'
start_title = 'GreenSeas Standards and Info'

status = check_link(start_url)  # Check functioning of start url

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

# Create lists for first run, to be written out to first sheet
first_run = [start_url]  # add the base url
first_titles = [start_title]  # add the base title
# Use extend function to add all urls and titles found in first run
first_run.extend(crawl_links(soup))
first_titles.extend(build_titles(soup))
# not being used as of 7/3/2014 but may be used later
# second_run = []
# second_titles = []

print('Creating xlsx file')
# Create excel file
wb = Workbook()
filename = 'Crawl.xlsx'
ws = wb.active
ws.title = 'First run'

max_first = len(first_run)
for row in ws.range('A1:A%s' % max_first):
    for cell in row:
        coord = coordinate_from_string(cell.coordinate)
        cell.value = first_titles[coord[1] - 1]

i = 0
for row in ws.range('B1:B%s' % (len(first_run) - 1)):
    for cell in row:
        cell.value = first_run[i]
        i += 1

ws1 = wb.create_sheet()
ws1.title = 'Second run'

first_run.pop(0)  # take off first in first_run (the start url)
for each in first_run:
    hText = (requests.get(each)).text
    crawlSoup = BeautifulSoup(hText)
    linksFound = crawl_links(crawlSoup)  # links found on a page
    titlesMade = build_titles(crawlSoup)
    # Place the source link above the list of links found
    source_row = ws1.get_highest_row() + 2
    ws1.cell('%s%s'%('B', source_row)).value = each
    if len(linksFound) > 0:
        start_row = ws1.get_highest_row() + 1
        last_row = (start_row + len(linksFound)) - 1
        t = 0
        for row in ws1.range('%s%s:%s%s' % ('A', start_row, 'A', last_row)):
            for cell in row:
                cell.value = titlesMade[t]
                t += 1
        k = 0
        for row in ws1.range('%s%s:%s%s' % ('B', start_row, 'B', last_row)):
            for cell in row:
                cell.value = linksFound[k]
                k += 1

print('broken links: {}'.format(brokenLinks))
print('Length of broken links: ' + str(len(brokenLinks)))
print('visited: {}'.format(visited))
print('Length of visited: ' + str(len(visited)))
print('Working urls: {}'.format(urls))
print('Length of urls: ' + str(len(urls)))
print('titles: {}'.format(titles))
print('Length of titles: ' + str(len(titles)))
wb.save(filename)
