from bs4 import BeautifulSoup
import requests
import re
from openpyxl import Workbook, cell
from openpyxl.styles import Style, Font
from urllib.request import urlopen
from urllib.error import URLError
import tldextract

# Http constant
HTTP = 'http://'
preFTP = 'ftp://'

# <editor-fold desc="Functions">

def crawl_links(soup):
    # Html tags to investigate
    urls_found = []
    for tag in soup.find_all('a', href=True):
        if HTTP in tag['href']:
            if tag['href'] not in visited:
                visited.append(tag['href'])
                # check functioning, will add to brokenLinks if link is bad
                check_link(tag['href'])
                # add to list of urls found
                if tag['href'] not in brokenLinks:
                    # add to list of working urls found to be written
                    urls_found.append(tag['href'])
                    # add to global list of working urls
                    urls.append(tag['href'])
        if preFTP in tag['href']:
            #urlopen(tag['href'])
            visited.append(tag['href'])
            # check functioning, will add to brokenLinks if link is bad
            # add to list of urls found
            if tag['href'] not in brokenLinks:
                # add to list of working urls found to be written
                urls_found.append(tag['href'])
                # add to global list of working urls
                urls.append(tag['href'])
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
    if check_type(url) == "HTTP":
        try:
            link = requests.get(url, timeout=10)
            c = link.status_code
        except requests.ConnectionError:
            works = 0
            print('{}: Connection error'.format(url))
            brokenLinks.append(url)
        except requests.Timeout:
            works = 0
            print('{}: Timeout error'.format(url))
            brokenLinks.append(url)
        except requests.TooManyRedirects:
            works = 0
            print('{}: Too Many Redirects'.format(url))
            brokenLinks.append(url)
        except requests.HTTPError:
            works = 0
            print('{}: HTTP Error'.format(url))
            brokenLinks.append(url)
        #except:
        #    works = 0
        #    print('{}: Unexpected Error'.format(url))
        #    brokenLinks.append(url)
        else:
            if c != 200:
                works = 0
                print('{}: Error code {}'.format(url, c))
                brokenLinks.append(url)
    elif check_type(url) == "FTP":
        try:
            urlopen(url)
        except URLError as e:
            works = 0
            print(url + ': ' + e.reason)
            brokenLinks.append(url)
    else:
        works = 0
        print('check link: {}'.format(check_type(url)))
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
    if check_type(url) == "FTP":
        return "None"
    if url not in brokenLinks and check_type(url) is "HTTP":
        getreq = requests.get(url)
        reqtext = getreq.text
        souper = BeautifulSoup(reqtext)
        # Search for all keywords, the values of the Domains dict
        for key in domainsKnown:
            for v in domainsKnown.get(key):
                # For all keywords found, filter so that only
                # the keywords in the page's visible text are found
                texts = souper.find_all(text=re.compile(v))
                visible_texts = filter(visible, texts)
                # For every keyword (value) found, add the Domain from our
                # dictionary (key) to the list fo domains associated with
                # the resource
                for vis in visible_texts:
                    # Added as a set to avoid duplicates
                    set_of_domains.add(key)
        # Turn the set of domains back into a list
        domains_found = list(set_of_domains)
    if len(domains_found) > 0:
        return domains_found
    else:
        return "None"


def find_resource_types(url):
    resos_found = []
    set_of_resources = set()
    if url not in brokenLinks and check_type(url) == "HTTP":
        getreq2 = requests.get(url)
        reqtext2 = getreq2.text
        souper2 = BeautifulSoup(reqtext2)
        for key in resourceTypesKnown:
            for v in resourceTypesKnown.get(key):
                texts = souper2.find_all(text=re.compile(v))
                visible_texts = filter(visible, texts)
                for vis in visible_texts:
                    set_of_resources.add(key)
        resos_found = list(set_of_resources)
    if len(resos_found) > 0:
        # print(str(resos_found))
        return resos_found
    else:
        return "None"


def find_organization(url):
    ext = tldextract.extract(url)
    extDom = ext.domain
    extSuff = ext.suffix
    newUrl = "http://" + extDom + "." + extSuff

    if check_link(newUrl) != 1:
        newUrl = "http://www." + extDom + "." + extSuff

    title = build_title(newUrl)
    if title is not None:
        return title
    else:
        return " "


def find_suffix(url):
    ext = tldextract.extract(url)
    # print(ext)
    extSuff = ext.suffix
    #print(extSuff)
    extDom = ext.domain
    #print(extSuff)
    #print(ext.domain + "." + extSuff)
    #for key in suffixesKnown:
    #       for v in suffixesKnown.get(key):
    #          if v in extSuff:
    #             return key
    if "com" in extSuff:
        return "Company"
    elif "edu" in extSuff:
        return "Education"
    elif "org" in extSuff:
        return "Non-profit Org"
    elif "gov" in extSuff:
        return "Government"
    elif "net" in extSuff:
        return "Internet service provider/Other network"


def find_country_code(url):
    ext = tldextract.extract(url)
    # print(ext)
    extSuff = ext.suffix

    if "uk" in extSuff:
        return "UK"
    elif "eu" in extSuff:
        return "European Union"
    elif "de" in extSuff:
        return "Germany"


def check_type(url):
    url_front = url[:url.index(':')]
    if url_front == "http" or url_front == "https":
        return "HTTP"
    elif url_front == "ftp":
        return "FTP"
    else:
        return " "


"""
Name: build_labels()
Params: url - page to get titles from
Purpose: Extract the title of the pages these links lead to
Returns: List of titles
"""


def build_title(url):
    working = check_link(url)
    if working == 1 and check_type(url) == "HTTP":
        var = requests.get(url)
        html = var.text
        title_soup = BeautifulSoup(html)
        page_title = None
        if url not in brokenLinks:
            if title_soup.title is not None:
                if title_soup.title.string is not None:
                    page_title = title_soup.title.string
            if page_title is not None:
                return page_title
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
    # if tag['href'] not in brokenLinks:
    # titles.append(tag.text)
    return titles_found

# </editor-fold>

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
domainsKnown = {'Agriculture/Farming': ["agriculture", "farming"], 'Atmosphere': ["atmosphere"],
                'Biology': ["biodiversity", "organism", "life science", "biota"],
                'Climate': ["climate"], 'Ecology': ["ecological", "ecosystem", "habitat", "environment"],
                'Geochemistry': ["geochem"],
                'Geology': ["geology", "geological"], 'GIS': ["geographic information systems"],
                'Marine Ecology': ["marine ecology", "oceanography"],
                'Marine Biology': ["marine biology"], 'Marine Geology': ["marine geology"],
                'Maps/Imagery': ["imaging", "maps"], 'Fisheries': ["estuaries", "fishing"],
                'Oceanography': ['ocean', 'sea'],
                'Spatial': ["spatial"], 'Topography': ["elevation", "mountains"]}

resourceTypesKnown = {'Activity': ["Conference"],
                      'Consensus Effort': ["Consortium", "Association", "Union"],
                      'Data Service': ["Network", "Services", "Tools", "Platform", "Infrastructure"],
                      'Catalog': ["search engine", "catalog"], 'Community': ["community"],
                      'Web Application': ["web application"],
                      'Portal': ["Visualization data", "Registry", "Infrastructure"],
                      'Specification': ["specification"],
                      'Image Collection': ["observation", "images", "gallery", "photography", "picture"],
                      'Web page': ["web page"],
                      'Interchange format': ["extension"],
                      'Vocabulary': ['vocabulary', 'vocab'],
                      'Service': ["spatial analysis", "spatial mapping"],
                      'Digital Repository': ["digital repository", "repository"],
                      'Functional Specification': ["functional specification", "queries of data"],
                      'Software': ["software", "code", "programming"],
                      'Forum': ["forum"], 'Organization': ["organization"]}

# start_url = 'http://www.greenseas.eu/content/standards-and-related-web-information'
#start_label = 'GreenSeas Home'
#start_title = 'Standards and Information'

start_url = 'http://cinergi.weebly.com/'
start_title = 'CINERGI Test Bed'
start_label = 'CINERGI Home'

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
#("First Run: " + str(first_run))
first_orgs = []
first_titles = []
# Use extend function to add all urls and titles found in first run
first_run.extend(crawl_links(soup))
first_labels.extend(build_labels(soup))
#first_orgs.extend(first_labels)
first_domains = [[]]
first_resource_types = []
first_content_types = []
first_tlds = []
first_country_codes = []

# not being used as of 7/3/2014 but may be used later
# second_run = []
# second_titles = []
for each in first_run:
    title = build_title(each)
    first_titles.append(title)
    first_domains.append(find_domains(each))
    first_resource_types.append(find_resource_types(each))
    first_content_types.append(check_type(each))
    first_tlds.append(find_suffix(each))
    #print("TLD: " + str(first_tlds))
    first_country_codes.append(find_country_code(each))
    first_orgs.append(find_organization(each))
    # print(first_orgs)

#print(first_domains)
print('Creating xlsx file')
# Create excel file
wb = Workbook()
filename = 'Crawl.xlsx'
ws = wb.active
ws.title = 'First run'

header_style = Style(font=Font(bold=True))
ws.cell('A1').value = 'Title'  # we need to find out how to do
ws['A1'].style = header_style
ws.cell('B1').value = 'Label'  # tag.text
ws['B1'].style = header_style
ws.cell('C1').value = 'URL'
ws['C1'].style = header_style
ws.cell('D1').value = 'Organization'
ws['D1'].style = header_style
ws['E1'].style = header_style
ws.cell('E1').value = 'Domain(s)'
ws.cell('F1').value = 'Resource Type'
ws['F1'].style = header_style
ws.cell('G1').value = "Content Type/Format"
ws['G1'].style = header_style
ws['H1'].value = "TLD"
ws['H1'].style = header_style
ws['I1'].value = "Country"
ws['I1'].style = header_style

max_first = len(first_titles) + 1
p = 0
for row in ws.range('A2:A%s' % max_first):  # 4
    for cell in row:
        cell.value = first_titles[p]
        p += 1

max_labels = len(first_labels)
p = 0
for row in ws.range('B2:B%s' % max_labels):
    for cell in row:
        cell.value = first_labels[p]
        p += 1

#("First Run: " + str(first_run))
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
first_domains.pop(0)
for row in ws.range('E2:E%s' % max_doms):
    for cell in row:
        if first_domains[q] != 'None':
            cell.value = ', '.join(first_domains[q])
        else:
            cell.value = first_domains[q]
        q += 1

max_cats = len(first_resource_types)
b = 0
for row in ws.range('F2:F%s' % max_cats):
    for cell in row:
        if first_resource_types[b] is not 'None':
            cell.value = ', '.join(first_resource_types[b])
        else:
            cell.value = str(first_resource_types[b])
        b += 1

max_cons = len(first_content_types)
s = 0
for row in ws.range('G2:G%s' % max_cons):
    for cell in row:
        cell.value = first_content_types[s]
        s += 1

max_tlds = len(first_tlds)
v = 0
for row in ws.range('H2:H%s' % max_tlds):
    for cell in row:
        cell.value = first_tlds[v]
        v += 1

max_cods = len(first_country_codes)
h = 0
for row in ws.range('I2:I%s' % max_cods):
    for cell in row:
        cell.value = first_country_codes[h]
        h += 1

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
    reTypes = []
    conTypes = []
    suffs = []
    cods = []

    for each in linksFound:
        titlesMade.append(build_title(each))
        domains.append(find_domains(each))
        reTypes.append(find_resource_types(each))
        conTypes.append(check_type(each))
        suffs.append(find_suffix(each))
        cods.append(find_country_code(each))
        orgsMade.append(find_organization(each))
        #print(orgsMade)

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
                cell.value = orgsMade[l]
                l += 1

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
                if reTypes[b] != "None":
                    cell.value = ', '.join(reTypes[b])
                else:
                    cell.value = str(reTypes[b])

        s = 0
        for row in ws1.range('%s%s:%s%s' % ('G', start_row, 'G', last_row)):
            for cell in row:
                if conTypes[s] != "None":
                    cell.value = conTypes[s]
                else:
                    cell.value = str(conTypes[s])
        d = 0
        for row in ws1.range('%s%s:%s%s' % ('H', start_row, 'H', last_row)):
            for cell in row:
                if suffs[d] != "None":
                    cell.value = suffs[d]
                else:
                    cell.value = str(suffs[d])
            d += 1

        h = 0
        for row in ws1.range('%s%s:%s%s' % ('I', start_row, 'I', last_row)):
            for cell in row:
                if cods[h] != "None":
                    cell.value = cods[h]
                else:
                    cell.value = str(cods[h])
            h += 1

        s += 1
        u += 1
        b += 1
    index += 1

# Apply headers (after data so as not to affect formula for skipping rows)
ws1.cell('A1').value = 'Title'
ws1.cell('B1').value = 'Label'
ws1.cell('C1').value = 'URL'
ws1.cell('D1').value = 'Organization'
ws1.cell('E1').value = 'Domain(s)'
ws1.cell('F1').value = 'Resource Type'
ws1.cell('G1').value = 'Content Type/Format'
ws1.cell('H1').value = "TLD"
ws1.cell('I1').value = "Country"
ws1['A1'].style = header_style
ws1['B1'].style = header_style
ws1['C1'].style = header_style
ws1['D1'].style = header_style
ws1['E1'].style = header_style
ws1['F1'].style = header_style
ws1['G1'].style = header_style
ws1['H1'].style = header_style
ws1['I1'].style = header_style

print('first orgs: {}'.format(orgsMade))
print('broken links: {}'.format(brokenLinks))
print('Length of broken links: ' + str(len(brokenLinks)))
print('visited: {}'.format(visited))
print('Length of visited: ' + str(len(visited)))
print('Working urls: {}'.format(urls))
print('Length of urls: ' + str(len(urls)))
print('titles: {}'.format(titles))
print('Length of titles: ' + str(len(titles)))
wb.save(filename)