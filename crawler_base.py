from bs4 import BeautifulSoup
import requests
import re
from openpyxl import Workbook, cell
from openpyxl.styles import Style, Font
# from openpyxl.cell import coordinate_from_string

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
    # build_labels(html_tags)
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

def visible(element):
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title', 'a']:
        return False
    elif re.match('<!--.*-->', str(element)):
        return False
    return True


def find_domains(url):
    domains_found = []
    set_of_domains = set()
    if url not in brokenLinks:
        getreq = requests.get(url)
        reqtext = getreq.text
        souper = BeautifulSoup(reqtext)
        for k in domainsKnown:
            for v in domainsKnown.get(k):
                texts = souper.find_all(text=re.compile(v))
                visible_texts = filter(visible, texts)
                for vis in visible_texts:
                    set_of_domains.add(k)
        domains_found = list(set_of_domains)
    if len(domains_found) > 0:
        return domains_found
    else:
        return "None"
                    #if vis.string:
                    #    print(vis.string)
                    #else:
                    #    print(vis)
def find_categories(url):
    categories_found = []
    set_of_categories = set()
    if url not in brokenLinks:
        getreq = requests.get(url)
        reqtext = getreq.text
        souper = BeautifulSoup(reqtext)
        for k in categoriesKnown:
            texts = souper.find_all(text=re.compile(k))
            visible_texts = filter(visible, texts)
            for vis in visible_texts:
                set_of_categories.add(k)
        categories_found = list(set_of_categories)
    if len(categories_found) > 0:
        #print("Categories found: " + categories_found)
        return categories_found
    else:
        return "None"
"""
Name: build_labels()
Params: url - page to get titles from
Purpose: Extract the title of the pages these links lead to
Returns: List of titles
"""

def build_title(url):
    status = check_link(url)
    if status == 1:
        var = requests.get(url)
        html = var.text
        soup = BeautifulSoup(html)
        title = None
        if url not in brokenLinks:
            if soup.title != None:
                if soup.title.string != None:
                    title = soup.title.string
            # findAll('title', limit = 1
            if title != None:
                return title
            else:
                return " "
    else:
        return " "

def build_labels(soup):
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
    # for tag in element_tags:
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
# Domains
domainsKnown = {'Agriculture/Farming': ["agriculture", "farming"], 'Atmosphere': ["atmosphere"], 'Biology':
    ["biodiversity", "organism", "life science", "biota"],
                'Climate': ["climate"], 'Ecology': ["ecological", "ecosystem", "habitat", "environment"],
                'Geochemistry': ["geochem"],
                'Geology': ["geology", "geological"], 'GIS': ["geographic information systems"],
                'Marine Ecology': ["marine ecology", "oceanography"],
                'Marine Biology': ["marine biology"], 'Marine Geology': ["marine geology"],
                'Maps/Imagery': ["imaging", "maps"], 'Fisheries': ["estuaries", "fishing"],
                'Oceanography': ['ocean', 'sea'],
                'Spatial': ["spatial"], 'Topography': ["elevation", "mountains"]}

categoriesKnown = {'Vocabulary', 'Catalog', 'Software', 'Information Model/Standard', 'Data Center', 'Community'}

start_url = 'http://www.greenseas.eu/content/standards-and-related-web-information'
start_label = 'GreenSeas Home'
start_title = 'Standards and Information'

#start_url = 'http://cinergi.weebly.com/'
#start_title = 'CINERGI Test Bed'
#start_label = 'CINERGI Home'

status = check_link(start_url)  # Check functioning of start url

tags = []

# Add start url link and title to lists
urls.append(start_url)
visited.append(start_url)
titles.append(start_title)

first_labels = []
first_labels.append(start_label)

if status:
    r = requests.get(start_url)
    htmlText = r.text
    soup = BeautifulSoup(htmlText)  # Make the soup
else:
    # exit if start url is broken
    exit()

# Create lists for first run, to be written out to first sheet
first_run = [start_url]  # add the base url
#first_labels = []
print("First Run: " + str(first_run))
first_orgs = []
first_titles = []
# Use extend function to add all urls and titles found in first run
first_run.extend(crawl_links(soup))
first_labels.extend(build_labels(soup))
first_orgs.extend(first_labels)
first_domains = [[]]
first_categories = []

# not being used as of 7/3/2014 but may be used later
# second_run = []
# second_titles = []
for each in first_run:
    title = build_title(each)
    first_titles.append(title)
    first_domains.append(find_domains(each))
    first_categories.append(find_categories(each))

print(first_domains)
print('Creating xlsx file')
# Create excel file
wb = Workbook()
filename = 'Crawl.xlsx'
ws = wb.active
ws.title = 'First run'

header_style = Style(font=Font(bold=True))
ws.cell('A1').value = 'Title' #we need to find out how to do
ws['A1'].style = header_style
ws.cell('B1').value = 'Label' #tag.text
ws['B1'].style = header_style
ws.cell('C1').value = 'URL'
ws['C1'].style = header_style
ws.cell('D1').value = 'Organization'
ws['D1'].style = header_style
ws['E1'].style = header_style
ws.cell('E1').value = 'Domain(s)'
ws.cell('F1').value = 'Category'
ws['F1'].style = header_style

max_first = len(first_titles) + 1
p = 0
for row in ws.range('A2:A%s' % max_first): #4
    for cell in row:
        cell.value = first_titles[p]
        p += 1

max_labels = len(first_labels)
p = 0
for row in ws.range('B2:B%s' % max_labels):
    for cell in row:
        cell.value = first_labels[p]
        p += 1

print("First Run: " + str(first_run))
i = 0
for row in ws.range('C2:C%s' % (len(first_run) + 1)):
    for cell in row:
        cell.value = first_run[i]
        i += 1

max_orgs = len(first_orgs)
n = 0
for row in ws.range('D2:D%s' % max_orgs):
    for cell in row:
        cell.value = first_orgs[n]
        n += 1

max_doms = len(first_domains)
q = 0
for row in ws.range('E2:E%s' % max_doms):
    for cell in row:
        cell.value = ', '.join(first_domains[q])
        q += 1

max_cats = len(first_categories)
b = 0
for row in ws.range('F2:F%s' % max_cats):
    for cell in row:
        cell.value = ', '.join(first_categories[b])
        b += 1

ws1 = wb.create_sheet()
ws1.title = 'Second run'

first_run.pop(0)  # take off first in first_run (the start url)
first_orgs.pop(0)
                  # We don't want GreenSeas to be in the second layer
index = 0
for each in first_run:
    hText = (requests.get(each)).text
    crawlSoup = BeautifulSoup(hText)
    linksFound = crawl_links(crawlSoup)  # links found on a page
    labelsMade = build_labels(crawlSoup)
    titlesMade = []
    org = first_orgs[index]
    orgsMade = []
    domains = []
    categories = []

    for each in linksFound:
        titlesMade.append(build_title(each))
        domains.append(find_domains(each))
        categories.append(find_categories(each))
    #for each in labelsMade:
        #orgsMade.append(each)

    # Place the source link above the list of links found
    # source_row = ws1.get_highest_row() + 2
    # ws1.cell('%s%s' % ('B', source_row)).value = each
    # ws1.cell('%s%s' % ('C', source_row)).value = 'source link'
    # ws1['%s%s'%('C', source_row)].style = header_style

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
                cell.value = labelsMade[k]
                k += 1
        j = 0
        for row in ws1.range('%s%s:%s%s' % ('C', start_row, 'C', last_row)):
            for cell in row:
                cell.value = linksFound[j]
                j += 1

        l = 0
        for row in ws1.range('%s%s:%s%s' % ('D', start_row, 'D', last_row)):
            for cell in row:
                cell.value = first_orgs[index]

        u = 0
        for row in ws1.range('%s%s:%s%s' % ('E', start_row, 'E', last_row)):
            for cell in row:
                if domains[u] != "None":
                    cell.value = ', '.join(domains[u])
                else:
                    cell.value = str(domains[u])

        b = 0
        for row in ws1.range('%s%s:%s%s' % ('F', start_row, 'F', last_row)):
            for cell in row:
                if categories[b] != "None":
                    cell.value = ', '.join(categories[b])
                else:
                    cell.value = str(categories[b])
        u += 1
        b += 1
    index += 1

# Apply headers (after data so as not to affect formula for skipping rows)
ws1.cell('A1').value = 'Title'
ws1.cell('B1').value = 'Label'
ws1.cell('C1').value = 'URL'
ws1.cell('D1').value = 'Organization'
ws1.cell('E1').value = 'Domain(s)'
ws1.cell('F1').value = 'Category'
ws1['A1'].style = header_style
ws1['B1'].style = header_style
ws1['C1'].style = header_style
ws1['D1'].style = header_style
ws1['E1'].style = header_style
ws1['F1'].style = header_style

print('broken links: {}'.format(brokenLinks))
print('Length of broken links: ' + str(len(brokenLinks)))
print('visited: {}'.format(visited))
print('Length of visited: ' + str(len(visited)))
print('Working urls: {}'.format(urls))
print('Length of urls: ' + str(len(urls)))
print('titles: {}'.format(titles))
print('Length of titles: ' + str(len(titles)))
wb.save(filename)