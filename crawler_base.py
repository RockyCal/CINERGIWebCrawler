from bs4 import BeautifulSoup
import requests
from openpyxl import Workbook, cell
from openpyxl.compat import range
from openpyxl.cell import get_column_letter, coordinate_from_string

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
            # check functioning
            check_link(tag['href'])
            # add to list of urls found
            if tag['href'] not in brokenLinks:
                urls_found.append(tag['href'])
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
    titles = []
    for tag in soup.find_all('a', href=True):
        if HTTP in tag['href']:
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
#print(first_run)

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

# May need work
i = 0
for row in ws.range('B1:B%s' % (len(first_run) - 1)):
    for cell in row:
        cell.value = first_run[i]
        i += 1

ws1 = wb.create_sheet()
ws1.title = "Second run"

curr = 0
#print(len(first_titles))
rowId = 2
for row in range(2, len(first_titles)):
    #coord = coordinate_from_string(cell.coordinate)
    #print(coord[1])
    if rowId % 2 == 0:
        print(first_titles[curr])
        ws1.cell('%s%s' % ('A', rowId)).value = first_titles[curr]
        curr += 1
        rowId += 2

#print(brokenLinks)
#id = 0
rowIdTitles = 1
rowIdLinks = 1
for each in first_run:
    if each not in brokenLinks:
        #print(each)
        hText = (requests.get(each)).text
        crawlSoup = BeautifulSoup(hText)
        # links found on page
        linksFound = crawl_links(crawlSoup)
        titles_made = build_titles(crawlSoup)
        second_run = second_run + linksFound
        second_titles = second_titles + titles_made

        max_second = len(linksFound)
        print("Length of links found: " + str(len(linksFound)))
        ind = 0
        #for row in range(1, max_second*2):
        #coord = coordinate_from_string(cell.coordinate)
        if rowIdTitles % 2 == 1:
            for col_idy in range(2, max_second):
                col = get_column_letter(col_idy)
                print("Col: " + str(col))
                print("Row: " + str(rowIdTitles))
                print("Title: " + str(titles_made[ind]))
                ws1.cell('%s%s' % (col, rowIdTitles)).value = titles_made[ind]
                ind += 1

        max_second = len(linksFound)
        ind = 0
        #for row in range(1, max_second*2):
        #coord = coordinate_from_string(cell.coordinate)
        if rowIdLinks % 2 == 0:
            for col_idy in range(2, max_second):
                col = get_column_letter(col_idy)
                ws1.cell('%s%s' % (col, rowIdLinks)).value = linksFound[ind]
                ind += 1

print(second_run)
#print(brokenLinks)
#print(second_run)
#for url in urls:
#    print(url)
#    hText = (requests.get(url)).text
#    crawlSoup = BeautifulSoup(hText)
#    visited.append(url)
#    urls.pop(0)
#    second_run = crawl_links(crawlSoup)


"""
for row in ws.range('B1:B%s' % (len(first_run) - 1)):
    for cell in row:
        cell.value = first_run[row-1]
"""

"""
curr = 0
for row in range(1, len(first_titles)):
    coord = coordinate_from_string(cell.coordinate)
    if coord[1] % 2 == 0:
        ws1.cell('%s%s' % (1, row)).value = first_titles[curr]
        curr += 1
    else:
        curr = curr

max_second = len(second_run)
ind = 0
for row in range(1, max_second*2):
    coord = coordinate_from_string(cell.coordinate)
    if coord[1] % 2 == 1:
        for col_idy in range(2, max_second):
            col = get_column_letter(col_idy)
            ws1.cell('%s%s' % (col, row)).value = second_titles[ind]
            ind += 1

max_second = len(second_run)
ind = 0
for row in range(1, max_second*2):
    coord = coordinate_from_string(cell.coordinate)
    if coord[1] % 2 == 0:
        for col_idy in range(2, max_second):
            col = get_column_letter(col_idy)
            ws1.cell('%s%s' % (col, row)).value = second_run[ind]
            ind += 1

id = -1
#Follows the links and crawls the sub-sites
for each in range(1, len(first_run)):
    #print(visited[each])
    id += 1

    curr = 0
    for row in range(1, len(first_titles)):
        coord = coordinate_from_string(cell.coordinate)
        if coord[1] % 2 == 0:
            ws1.cell('%s%s' % (1, row)).value = first_titles[curr]
            curr += 1
        else:
            curr = curr

    max_second = len(second_run)
    ind = 0
    for row in range(1, max_second*2):
        coord = coordinate_from_string(cell.coordinate)
        if coord[1] % 2 == 1:
            for col_idy in range(2, max_second):
                col = get_column_letter(col_idy)
                ws1.cell('%s%s' % (col, row)).value = second_titles[ind]
                ind += 1

    max_second = len(second_run)
    ind = 0
    for row in range(1, max_second*2):
        coord = coordinate_from_string(cell.coordinate)
        if coord[1] % 2 == 0:
            for col_idy in range(2, max_second):
                col = get_column_letter(col_idy)
                ws1.cell('%s%s' % (col, row)).value = second_run[ind]
                ind += 1

"""
print('visited: {}'.format(visited))
print('Length of visited: ' + str(len(visited)))
print('broken links: {}'.format(brokenLinks))
print('Length of broken links: ' + str(len(brokenLinks)))
print('urls: {}'.format(urls))
print('titles: {}'.format(titles))
wb.save(filename)
