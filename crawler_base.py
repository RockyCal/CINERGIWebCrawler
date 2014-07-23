from bs4 import BeautifulSoup
import requests
import re
from openpyxl import Workbook, cell
from openpyxl.styles import Style, Font
from urllib.request import urlopen
from urllib.error import URLError
import tldextract

# <editor-fold desc="Protocol constants">
HTTP = 'http://'
preFTP = 'ftp://'
# </editor-fold>

# <editor-fold desc="class Resource">
class Resource:
    def __init__(self, url):
        self.link = url
    title = 'No title'
    url_type = 'Type not identified'
    org = 'Organization not found'
    disciplines = []
    resource_type = []

# </editor-fold>

# <editor-fold desc="Functions">
def check_type(url):
    url_front = url[:url.index(':')]
    if url_front == "http" or url_front == "https":
        return "HTTP"
    elif url_front == "ftp":
        return "FTP"
    else:
        return "None"


def check_again(new_url):
    try:
        rq = requests.get(new_url)
        cq = rq.status_code
    except requests.ConnectionError:
        # fixed = 0
        print('{}: Connection error'.format(new_url))
        brokenLinks.append(new_url)
        return " "
    except requests.Timeout:
        # fixed = 0
        print('{}: Timeout error'.format(new_url))
        brokenLinks.append(new_url)
        return " "
    except requests.TooManyRedirects:
        # fixed = 0
        print('{}: Too Many Redirects'.format(new_url))
        brokenLinks.append(new_url)
        return " "
    except requests.HTTPError:
        # fixed = 0
        print('{}: HTTP Error'.format(new_url))
        brokenLinks.append(new_url)
        return " "
    else:
        if cq != 200:
            # fixed = 0
            print('{}: Error code {}'.format(new_url, cq))
            brokenLinks.append(new_url)
            return " "
    return new_url


"""
Name: check_link()
Params: url - link to check
Purpose: Make sure links work and go somewhere
Returns: 1 if link works w/o error
         Exits if link is broken
"""

def check_link(url):
    works = url
    if check_type(url) == "HTTP":
        try:
            link = requests.get(url, timeout=10)
            c = link.status_code
        except requests.ConnectionError:
            if "www." in url:
                works = " "
                print('{}: Connection error'.format(url))
                brokenLinks.append(url)
            else:
                # If www not in link, add it to link and see if it works
                ext_url = tldextract.extract(url)
                url_sub = ext_url.subdomain
                url_dom = ext_url.domain
                url_suff = ext_url.suffix
                new_url = "http://www." + url_sub + url_dom + "." + url_suff
                return check_again(new_url)
        except requests.Timeout:
            works = " "
            print('{}: Timeout error'.format(url))
            brokenLinks.append(url)
        except requests.TooManyRedirects:
            works = " "
            print('{}: Too Many Redirects'.format(url))
            brokenLinks.append(url)
        except requests.HTTPError:
            works = " "
            print('{}: HTTP Error'.format(url))
            brokenLinks.append(url)
        else:
            if c != 200:
                works = " "
                print('{}: Error code {}'.format(url, c))
                brokenLinks.append(url)
    elif check_type(url) == "FTP":
        works = url
        try:
            urlopen(url)
        except URLError as e:
            works = " "
            print(url + ': ' + e.reason)
            brokenLinks.append(url)
    else:
        works = " "
        print('check link: {}'.format(check_type(url)))
    return works

def visible(element):
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title', 'a']:
        return False
    elif re.match('<!--.*-->', str(element)):
        return False
    return True

def find_links(this_url):
    urls_found = []
    get = requests.get(this_url)
    h_text = get.text
    soup = BeautifulSoup(h_text)
    for link_tag in soup.find_all('a', href=True):
        if HTTP in link_tag['href'] or preFTP in link_tag['href']:
            url_correct = check_link(link_tag['href'])
            if url_correct is not " ":
                urls_found.append(url_correct)
    return urls_found


def find_disciplines(url):
    disciplines_found = []
    set_of_disciplines = set()
    if check_type(url) is "FTP":
        return "None"
    if check_type(url) is "HTTP":
        souper = BeautifulSoup(requests.get(url).text)
        # Search for all keywords, the values of the Domains dict
        for key in disciplinesKnown:
            for v in disciplinesKnown.get(key):
                # For all keywords found, filter so that only
                # the keywords in the page's visible text are found
                texts = souper.find_all(text=re.compile(v))
                visible_texts = filter(visible, texts)
                # For every keyword (value) found, add the Domain from our
                # dictionary (key) to the list fo domains associated with
                # the resource
                for vis in visible_texts:
                    # Added as a set to avoid duplicates
                    set_of_disciplines.add(key)
        # Turn the set of domains back into a list
        disciplines_found = list(set_of_disciplines)
    if len(disciplines_found) > 0:
        return disciplines_found
    else:
        return ['No disciplines found']


def find_resource_types(url):
    resos_found = []
    set_of_resources = set()
    if check_type(url) is "HTTP":
        souper2 = BeautifulSoup(requests.get(url).text)
        for key in resourceTypesKnown:
            for v in resourceTypesKnown.get(key):
                texts = souper2.find_all(text=re.compile(v))
                visible_texts = filter(visible, texts)
                for vis in visible_texts:
                    set_of_resources.add(key)
        resos_found = list(set_of_resources)
    if len(resos_found) > 0:
        return resos_found
    else:
        return ['None']


def find_organization(url):
    basic_org = build_title(url)

    if basic_org in orgsOfficial:
        return "Verified: " + basic_org
    elif build_title(url) is not 'No title':
        return build_title(url)
    else:
        return "NA"


def find_suffix(url):
    ext = tldextract.extract(url)
    # print(ext)
    suff = ext.suffix
    if "com" in suff:
        return "Company"
    elif "edu" in suff:
        return "Education"
    elif "org" in suff:
        return "Non-profit Org"
    elif "gov" in suff:
        return "Government"
    elif "net" in suff:
        return "Internet service provider/Other network"

def find_country_code(url):
    ext = tldextract.extract(url)
    # print(ext)
    suffix = ext.suffix
    for each in countriesOfficial:
        str2 = str(each)
        str2 = str2.lower()
        print(str2)
        if suffix in str2[:5]:
            #if ext:
            print(suffix + " = " + str2)
            return str2.upper()

def find_social_media(url):
    title = build_title(url)
    retStatement = ""
    for each in socialMedia:
        if each in title:
            return each

def find_term_links(string):
    retUrl = []

    # Domains
    for each in string:
        if("Agriculture/Farming" in string):
            retUrl.append("http://cinergiterms.weebly.com/uploads/7/5/1/1/7511984/agr.jpg, ")
        if("Biology" in string):
            retUrl.append("http://cinergiterms.weebly.com/uploads/7/5/1/1/7511984/bio.jpg, ")

        # Resource Types
        if("Catalog" in string):
            retUrl.append("http://cinergiterms.weebly.com/uploads/7/5/1/1/7511984/catalog.jpg, ")
        if("Community" in string):
            retUrl.append("http://cinergiterms.weebly.com/uploads/7/5/1/1/7511984/community.jpg, ")

    return retUrl


def link_type(url):
    if url not in brokenLinks:
        getreq2 = requests.get(url)
        reqtext2 = getreq2.text
        souper2 = BeautifulSoup(reqtext2)
        LinkString = ""
        if souper2.find("form")!= None:
            LinkString += "search engine/"
        if souper2.find(["download" or "programs" or 'software'])!= None:
            LinkString += "download"
        if souper2.find("<p>" > "HREF")!= None:
            LinkString += "information"
        if souper2.find(["request", "login", "order", "purchase"])!= None:
            LinkString += "offlineAccess"
        return LinkString

"""
        if souper2.find("form")!= None:
                    return 'search engine'
        elif souper2.find(["download" or "programs" or 'software'])!= None:
                    return 'download'
        elif souper2.find("<p>" > "HREF")!= None:
                    return 'information'
        elif souper2.find(text="Data",HREF= True):
            if souper2.find(text=["request", "login", "order", "purchase"]):
                    return 'offlineAccess'

"""
"""
Name: build_labels()
Params: url - page to get titles from
Purpose: Extract the title of the pages these links lead to
Returns: List of titles
"""
# titles -> texts
def build_text(soup):
    texts = []
    for tag in soup.find_all('li'):
        texts.append(tag.text)
    return texts


def build_title(page_url):
    page_text = BeautifulSoup((requests.get(page_url)).text)
    for title in page_text.find_all('title'):
        if title.has_attr('string'):
            return title.string
        else:
            return title.text
def build_social_links(soup):
    links = []
    for tag in soup.find_all('th'):
        links.append(tag.text)
    return links



def build_labels(soup):
    titles_found = []
    for tag in soup.find_all('a', href=True):
        if HTTP in tag['href']:
            if tag['href'] not in brokenLinks:
                titles_found.append(tag.text)
                # add to list of total titles
                titles.append(tag.text)
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
disciplinesKnown = {'Agriculture/Farming': ["agriculture", "farming"], 'Atmosphere': ["atmosphere"],
                'Biology': ["biodiversity", "organism", "life science", "biota"],
                'Climate': ["climate"], 'Ecology': ["ecological", "ecosystem", "habitat", "environment"],
                'Geochemistry': ["geochem"],
                'Geology': ["geology", "geological"], 'GIS': ["geographic information systems"],
                'Marine Ecology': ["marine ecology", "oceanography"],
                'Marine Biology': ["marine biology"], 'Marine Geology': ["marine geology"],
                'Maps/Imagery': ["imaging", "maps"], 'Fisheries': ["estuaries", "fishing"],
                'Oceanography': ["ocean", "sea"],
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

start_url = 'http://www.greenseas.eu/content/standards-and-related-web-information'
start_label = 'GreenSeas Home'
start_title = 'Standards and Information'

#start_url = 'http://cinergi.weebly.com/'
#start_title = 'CINERGI Test Bed'
#tart_label = 'CINERGI Home'

#start_url = 'http://www.antarctica.ac.uk/dms/'
#start_title = "Antarctica"
#start_label = 'Antartica Home'

# List of organizations
org_url = 'http://opr.ca.gov/s_listoforganizations.php'
# List of country codes
country_codes_url = 'http://www.thrall.org/domains.htm'
social_media_url = 'http://en.wikipedia.org/wiki/List_of_social_networking_websites#L'

# Add to urls visited
status = check_link(start_url)  # Check functioning of start url
statusOrgs = check_link(org_url)
statusCountryCodes = check_link(country_codes_url)
statusSocUrls = check_link(social_media_url)

tags = []

# Add start url link and title to lists
urls.append(start_url)
visited.append(start_url)

# Check functioning of start url
if check_link(start_url) is " ":
    # exit if start url is broken
    exit()

# Add to list of working urls
urls.append(start_url)

# Check functioning of organizations list
if check_link(org_url) is not " ":
    t = requests.get(org_url)
    orgText = t.text
    soupOrg = BeautifulSoup(orgText)

# Check functioning of country codes list
if check_link(country_codes_url) is not " ":
    s = requests.get(country_codes_url)
    counText = s.text
    soupCoun = BeautifulSoup(counText)
    #print(soupCoun)
if statusSocUrls != " ":
    b = requests.get(social_media_url)
    socText = b.text
    soupSoc = BeautifulSoup(socText)

orgsOfficial = build_labels(soupOrg)
countriesOfficial = build_text(soupCoun)
countriesOfficial.append("EU - European Union")
socialMedia = build_social_links(soupSoc)

# What is this? # The countries list we are using does not have EU

# TODO: what is this doing?
# the countries list has four at the beginning that aren't countries - which is why they are popped off
for t in range(0, 4):
    countriesOfficial.pop(0)

# Create first resource
res0 = Resource(start_url)
start_html = (requests.get(start_url)).text
start_soup = BeautifulSoup(start_html)
res0.title = build_title(start_url)
res0.url_type = check_type(res0.link)
# First run
links_found = find_links(start_url)
first_run = [res0]

# Build the resources from the links found
for alink in links_found:
    url_final = check_link(alink)  # named so b/c url may be changed in function
    res = Resource(url_final)
    res.link = url_final
    if res.link is not " ":
        res.url_type = check_type(url_final)
        if res.url_type is 'HTTP':
            # commented out for soup-making amendment to build_title
            #html = (requests.get(res.link)).text
            #sewp = BeautifulSoup(html)
            res.title = build_title(res.link)
            res.org = find_organization(res.link)
            res.disciplines = find_disciplines(res.link)
            res.resource_type = find_resource_types(res.link)
            titles.append(res.title)
            urls.append(res.link)
            first_run.append(res)
        elif res.url_type is 'FTP':
            res.title = 'FTP site'
            first_run.append(res)
    else:
        brokenLinks.append(alink)

# <editor-fold desc="Excel Sheet 1">
print('Creating xlsx file')
# Create excel file
wb = Workbook()
filename = 'Crawl_with_Class.xlsx'
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
ws['J1'].value = "Social Media?"
ws['J1'].style = header_style
ws['K1'].value = "Term Definitions"
ws['K1'].style = header_style

j = 2
for resource in first_run:
    ws['A%s' % j].value = resource.title
    # ws['B%s' % j].value = resource.label  # no label assigned
    ws['C%s' % j].value = resource.link
    ws['D%s' % j].value = resource.org
    ws['E%s' % j].value = ', '.join(sorted(resource.disciplines))
    ws['F%s' % j].value = ','.join(sorted(resource.resource_type))
    ws['G%s' % j].value = resource.url_type
    j += 1

# </editor-fold>


# <editor-fold desc="Second Run">
ws1 = wb.create_sheet()
ws1.title = 'Second run'

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
ws1.cell('J1').value = "Social Media Link"
ws1['A1'].style = header_style
ws1['B1'].style = header_style
ws1['C1'].style = header_style
ws1['D1'].style = header_style
ws1['E1'].style = header_style
ws1['F1'].style = header_style
ws1['G1'].style = header_style
ws1['H1'].style = header_style
ws1['I1'].style = header_style
ws1['J1'].style = header_style
# </editor-fold>

ws2 = wb.create_sheet()
ws2.title = 'List of Official Organizations'
if len(orgsOfficial) > 0:
    start_row = ws2.get_highest_row() + 1
    last_row = (start_row + len(orgsOfficial)) - 1
    t = 0
    for row in ws2.range('%s%s:%s%s' % ('A', start_row, 'A', last_row)):
        for cell in row:
            cell.value = orgsOfficial[t]
            t += 1

ws3 = wb.create_sheet()
ws3.title = 'List of Country Codes'
if len(countriesOfficial) > 0:
    start_row = ws3.get_highest_row() + 1
    last_row = (start_row + len(countriesOfficial)) - 1
    t = 0
    for row in ws3.range('%s%s:%s%s' % ('A', start_row, 'A', last_row)):
        for cell in row:
            cell.value = countriesOfficial[t]
            t += 1

#print('first orgs: {}'.format(orgsMade))
print('broken links: {}'.format(brokenLinks))
#print('visited: {}'.format(visited))
#print('Length of visited: ' + str(len(visited)))
print('Working urls: {}'.format(urls))
#print('Length of urls: ' + str(len(urls)))
#print('titles: {}'.format(titles))
#print('Length of titles: ' + str(len(titles)))
wb.save(filename)