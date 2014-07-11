from bs4 import BeautifulSoup
import requests
import re
from openpyxl import Workbook, cell
from openpyxl.styles import Style, Font
import tldextract
from openpyxl.cell import coordinate_from_string

# Http constant
HTTP = 'http://'

def crawl_links(soup):
    # Html tags to investigate
    urls_found = []
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
    # build_labels(html_tags)
    return urls_found

    #returns co.uk for forums.bbc.co.uk

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
    # print(url)
    if url not in brokenLinks:
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
    if url not in brokenLinks:
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

def find_suffix(url):
    ext = tldextract.extract(url)
    #print(ext)
    extSuff = ext.suffix
    # print(extSuff)
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
    #print(ext)
    extSuff = ext.suffix

    if "uk" in extSuff:
        return "UK"
    elif "eu" in extSuff:
        return "European Union"
    elif "de" in extSuff:
        return "Germany"

def check_type(url):
    url_front = url[:url.index('p') + 1]
    if url_front == "http":
        return "HTTP"
    elif url_front == "ftp":
        return "FTP"


"""
Name: build_labels()
Params: url - page to get titles from
Purpose: Extract the title of the pages these links lead to
Returns: List of titles
"""


def build_title(url):
    working = check_link(url)
    if working == 1:
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

#start_url = 'http://www.greenseas.eu/content/standards-and-related-web-information'
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
# print("First Run: " + str(first_run))
first_orgs = []
first_titles = []
# Use extend function to add all urls and titles found in first run
first_run.extend(crawl_links(soup))
first_labels.extend(build_labels(soup))
first_orgs.extend(first_labels)
first_domains = [[]]
first_resource_types = []
first_content_types = []
first_tlds = []
first_country_codes = []

print('Creating xlsx file')
# Create excel file
wb = Workbook()
filename = 'Crawl.xlsx'
ws = wb.active
ws.title = 'First run'
ws1 = wb.create_sheet()
ws1.title = 'Second run'

# not being used as of 7/3/2014 but may be used later
# second_run = []
# second_titles = []
start_row = ws.get_highest_row() # 2
rownum = 2
index = 0
for each in first_run:
    title = build_title(each)
    ws['A%s'%(rownum)].value = title
    ws['C%s'%(rownum)].value = each
    #first_titles.append(title)
    if find_domains(each) is not 'None':
        ws['E%s'%(rownum)].value = ','.join(find_domains(each))
    else:
        ws['E%s'%(rownum)].value = 'None'
    if find_resource_types(each) is not 'None':
        ws['F%s'%(rownum)].value = ','.join(find_resource_types(each))
    else:
        ws['F%s'%(rownum)].value = 'None'
    # first_resource_types.append(find_resource_types(each))
    ws['G%s'%(rownum)].value = check_type(each)
    #first_content_types.append(check_type(each))
    ws['H%s'%(rownum)].value = find_suffix(each)
    # first_tlds.append(find_suffix(each))
    ws['I%s'%(rownum)].value = find_country_code(each)
    # first_country_codes.append(find_country_code(each))

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

    if len(linksFound) > 0:
        start_row = ws1.get_highest_row() + 1
        last_row = (start_row + len(linksFound)) - 1

        k = 0
        for row in ws1.range('%s%s:%s%s' % ('B', start_row, 'B', last_row)):
            for cell in row:
                cell.value = labelsMade[k]
                k += 1

        g = 0
        for row in ws1.range('%s%s:%s%s' % ('D', start_row, 'D', last_row)):
            for cell in row:
                cell.value = first_orgs[index]
                g += 1

    row = 2
    for each in linksFound:
        title = build_title(each)
        ws1['A%s'%(row)].value = title
        ws1['C%s'%(row)].value = each
        #first_titles.append(title)
        if find_domains(each) is not 'None':
            ws1['E%s'%(row)].value = ', '.join(find_domains(each))
        else:
            ws1['E%s'%(row)].value = 'None'
        if find_resource_types(each) is not 'None':
            ws1['F%s'%(row)].value = ', '.join(find_resource_types(each))
        else:
            ws1['F%s'%(row)].value = 'None'
        # first_resource_types.append(find_resource_types(each))
        ws1['G%s'%(row)].value = check_type(each)
        #first_content_types.append(check_type(each))
        ws1['H%s'%(row)].value = find_suffix(each)
        # first_tlds.append(find_suffix(each))
        ws1['I%s'%(row)].value = find_country_code(each)
        # first_country_codes.append(find_country_code(each))
        row += 1

    #index += 1
    rownum += 1

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


max_labels = len(first_labels)
p = 0
for row in ws.range('B2:B%s' % max_labels):
    for cell in row:
        cell.value = first_labels[p]
        p += 1

max_orgs = len(first_orgs)
n = 0
for row in ws.range('D2:D%s' % max_orgs):
    for cell in row:
        cell.value = first_orgs[n]
        n += 1

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

print('broken links: {}'.format(brokenLinks))
print('Length of broken links: ' + str(len(brokenLinks)))
print('visited: {}'.format(visited))
print('Length of visited: ' + str(len(visited)))
print('Working urls: {}'.format(urls))
print('Length of urls: ' + str(len(urls)))
print('titles: {}'.format(titles))
print('Length of titles: ' + str(len(titles)))
wb.save(filename)