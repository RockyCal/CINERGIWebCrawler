from bs4 import BeautifulSoup
import requests
import re
import queue
from openpyxl import Workbook, cell
from openpyxl.styles import Style, Font
from urllib.request import urlopen, Request
from urllib.error import URLError
import urllib.parse
from check_link import check_link
import tldextract
import threading
from disciplines_known import disciplinesKnown
from resourceTypes import resourceTypesKnown
from write import write_resource
import time
from urllib.parse import urljoin

# <editor-fold desc="Protocol constants">
HTTP = 'http://'
preFTP = 'ftp://'
# </editor-fold>


class Thread(threading.Thread):
    def __init__(self, stack, tier, count, delay):
        threading.Thread.__init__(self)
        self.stack = stack
        self.tier = tier
        self.count = count
        self.delay = delay

    def run(self):
        crawl(self.stack, self.tier, self.delay)


class ThreadClass(threading.Thread):
    def __init__(self, que, count, delay):
        threading.Thread.__init__(self)
        self.queue = que
        self.count = count
        self.delay = delay

    def run(self):
        while True:
            items = self.queue.get()
            stack = items[0]
            new_tier = items[1]
            crawl(stack, new_tier, self.delay)
            self.queue.task_done()


# <editor-fold desc="class Resource">
class Resource:
    def __init__(self, url):
        link_status = check_link(url)
        if link_status is "working":
            self.link = url
            self.status = link_status
        else:
            if 'www' not in url:
                ext_url = tldextract.extract(url)
                url_sub = ext_url.subdomain
                url_dom = ext_url.domain
                suff = url.split(ext_url.suffix)
                url_suff = ext_url.suffix + suff[1]
                link = "http://www." + url_sub + url_dom + "." + url_suff
                link_status = check_link(link)
                if link_status is "working":
                    self.link = link
                    self.status = link_status
            else:
                brokenLinks.append(url)
                self.link = link_status
                self.status = link_status

    text = ""
    title = "No title"
    status = "No status"
    resource_type = []
    themes = []
    org = "Organization not found"
    resource_contact_person_name = ""
    resource_contact_org = ""
    resource_contact_email = ""
    resource_contact_phone = ""
    url_type = "Type not identified"
    tld = ""
    country_code = ""
    social_media = ""
    links_found = []

    def get_resource_data(self):
        self.title = build_title(self.link)
        self.resource_type = find_resource_types(self.link)
        self.themes = find_themes(self.link)
        self.org = find_organization(self.link)
        find_contact_info(self, self.link)
        # self.url_type = check_type(self.link)
        # self.tld = find_suffix(self.link)
        # self.country_code = find_country_code(self.link)
        self.social_media = find_social_media(self.link)

    def find_links(self):
        if self.status is "working":
            try:
                soup = BeautifulSoup(urlopen(self.link, timeout=7).read())
                for link_tag in soup.find_all('a', href=True):
                    if check_link(link_tag['href']) is not "working":
                        new_url = urljoin(self.link, link_tag['href'])
                        if check_link(new_url) is "working" and new_url != self.link:
                            if new_url not in self.links_found:
                                self.links_found.append(new_url)
                    else:
                        if link_tag['href'] != self.link:
                            if link_tag['href'] not in self.links_found:
                                self.links_found.append(link_tag['href'])
            except URLError as e:
                self.status = "{} {} {}".format(self.link, e.reason)
                brokenLinks.append(self.link)

# <editor-fold desc="Functions">

"""
name: crawl
stack is stack of links
"""


def crawl(stack, new_tier, delay):
    while len(stack) > 0:
        # Make instance of Resource
        resource = Resource(stack.pop(0))
        if resource.status is "working":
            urlopen(resource.link)
            if resource.link not in visited:
                resource.get_resource_data()
                visited.append(resource.link)
                new_tier.append(resource)
        time.sleep(delay)


def make_headers(sheet):
    header_style = Style(font=Font(bold=True))
    sheet.cell('A1').value = 'Title'  # we need to find out how to do
    sheet['A1'].style = header_style
    sheet.cell('B1').value = 'URL'
    sheet['B1'].style = header_style
    sheet.cell('C1').value = 'Organization'
    sheet['C1'].style = header_style
    sheet['D1'].style = header_style
    sheet.cell('D1').value = 'Theme(s)'
    sheet.cell('E1').value = 'Resource Type'
    sheet['E1'].style = header_style
    sheet['F1'].value = "Country"
    sheet['F1'].style = header_style
    sheet['G1'].value = "Social Media?"
    sheet['G1'].style = header_style
    sheet['H1'].value = "Term Definitions"
    sheet['H1'].style = header_style


def check_type(url):
    url_front = url[:url.index(':')]
    if url_front == "http" or url_front == "https":
        return "HTTP"
    elif url_front == "ftp":
        return "FTP"
    else:
        return "None"


"""
Name: check_link()
Params: url - link to check
Purpose: Make sure links work and go somewhere
Returns: Returns working link if works or
         returns None
"""


def visible(element):
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title', 'a']:
        return False
    elif re.match('<!--.*-->', str(element)):
        return False
    return True

def find_themes(url):
    disciplines_found = []
    set_of_disciplines = set()
    if check_type(url) is "FTP":
        return "None"
    if check_type(url) is "HTTP":
        souper = BeautifulSoup(urlopen(url).read())
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
    set_of_resources = set()
    souper2 = BeautifulSoup(urlopen(url).read())
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

    verify_url = "https://orcid.org/orcid-search/quick-search"
    data = {'searchQuery': basic_org}
    url_values = urllib.parse.urlencode(data)
    full_url = verify_url + '?' + url_values
    response = urllib.request.urlopen(full_url)
    soup = BeautifulSoup(urlopen(full_url).read())
    no_result_text = soup.find(text=re.compile('No results found'))
    if visible(no_result_text):
        return basic_org
    else:
        return "Verified: " + basic_org

    #if basic_org in orgsOfficial:
    #    return "Verified: " + basic_org
    #elif basic_org is not 'No title':
    #    return basic_org


def find_suffix(url):
    ext = tldextract.extract(url)
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
    suffix = ext.suffix
    for ea in countriesOfficial:
        str2 = str(ea)
        str2 = str2.lower()
        if suffix in str2[:5]:
            # if ext:
            return str2.upper()


def find_social_media(url):
    title = build_title(url)
    ret_statement = ""
    if title is not None:
        for soc in socialMedia:
            if soc in title:
                return soc
                # possible else: return ret_statement
    else:
        return ret_statement


def link_type(url):
    souper2 = BeautifulSoup(urlopen(url).read())
    link_string = ""
    if souper2.find("form") is not None:
        link_string += "search engine"
    if souper2.find(["download" or "programs" or 'software']) is not None:
        link_string += "download"
    if souper2.find("<p>" > "HREF") is not None:
        link_string += "information"
    if souper2.find(["request", "login", "order", "purchase"]) is not None:
        link_string += "offlineAccess"
    return link_string


def find_home_page(url):
    ext = tldextract.extract(url)
    ext_dom = ext.domain
    ext_suff = ext.suffix
    new_url = "http://www." + ext_dom + "." + ext_suff
    new_url = new_url.strip('/')
    return new_url


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


def build_title(url):
    req = Request(url)
    page_text = BeautifulSoup(urlopen(req).read())
    title = page_text.find('title', text=True)
    if title is not None:
        if title.has_attr('string'):
            return title.string
        else:
            return title.text
    return 'No title'


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


def find_contact_info(reso, url):
    page = BeautifulSoup(urlopen(url).read())
    contact = page.find(text=re.compile('Contact/i'))
    if contact is not None:
        if 'href' in contact:
            if check_link(contact['href']) is "working":
                page = BeautifulSoup(urlopen(contact['href']).read())
    # first look for tag with class = phone
    phone = page.find({'class': 'phone'})
    if phone is not None:
        reso.resource_contact_phone = phone.text
    else:
        # if not class = phone, look for phone number
        phone = page.find(text=re.compile('\+(9[976]\d|8[987530]\d|6[987]\d'
                                          '|5[90]\d|42\d|3[875]\d|2[98654321]'
                                          '\d|9[8543210]|8[6421]|6[6543210]|5'
                                          '[87654321]|4[987654310]|3[9643210]'
                                          '|2[70]|7|1)\d{1,14}$'))
        if phone is not None:
            print(phone)
            reso.resource_contact_phone = phone.text
    email = page.find({'class': 'email'})
    if email is not None:
        reso.resource_contact_email = email.text
    else:
        email = page.find(text=re.compile('\b[A-Z0-9._%+-]+[@(at)][A-Z0-9.-]+\.[A-Z]{2,4}\b'))
        if email is not None:
            reso.resource_contact_email = email.text


# </editor-fold>

"""
Program begins.
"""
# Total visited links
visited = []
# Total working links found
urls = []
# Total broken links
brokenLinks = []

titles = []

# Create excel file
wb = Workbook()
filename = input("Enter a title for the excel file: ")
#filename = 'GreenSeas_9_15.xlsx'

# <editor-fold desc="Build org, country, social media">
# List of organizations
org_url = 'http://opr.ca.gov/s_listoforganizations.php'
# List of country codes
country_codes_url = 'http://www.thrall.org/domains.htm'
social_media_url = 'http://en.wikipedia.org/wiki/List_of_social_networking_websites#L'

# Check functioning of organizations list
if check_link(org_url) is "working":
    t = requests.get(org_url)
    orgText = t.text
    soupOrg = BeautifulSoup(orgText)
    orgsOfficial = build_labels(soupOrg)

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
else:
    print("Error with org url")

# Check functioning of country codes list
if check_link(country_codes_url) is "working":
    s = requests.get(country_codes_url)
    counText = s.text
    soupCoun = BeautifulSoup(counText)
    countriesOfficial = build_text(soupCoun)
    countriesOfficial.append("EU - European Union")
    # Get rid of first four, random values
    for t in range(0, 4):
        countriesOfficial.pop(0)

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
else:
    print("Error with country codes url")

if check_link(social_media_url) is "working":
    b = requests.get(social_media_url)
    socText = b.text
    soupSoc = BeautifulSoup(socText)
    socialMedia = build_social_links(soupSoc)
else:
    print("Error with social media url")

# </editor-fold>

"""
Resources is the list of actual resources
"""
resources = []
"""
Tiers are levels of link crawling. The start url is tier0.
The links on the page of the start url are tier1. All the links
on all the pages of those urls in tier1 are tier2. And so on.
The first link of every tier is the source link
"""
tiers = []

all_visited = []

prompt = input("Enter 1) to crawl for data and find other links from a single start point. Enter 2) to "
               "scrape data from a list of links: ")
mode = int(prompt)


if mode is 1:
    start_url = input("Enter a start url to begin crawl: ")
    # If start_url is broken program exits
    if check_link(start_url) is not "working":
        print("Error with start url.")
        exit()

    # Create first resource
    res0 = Resource(start_url)
    visited.append(start_url)
    res0.text = BeautifulSoup(urlopen(start_url).read())
    print("Crawling...")
    # Scrape source url
    res0.get_resource_data()
    # Find links on source url web page,
    # will be crawled and become tier1
    res0.find_links()
    print("Length of res0.links_found: {}".format(len(res0.links_found)))
    tier0 = [res0]
    # Set up for crawl
    resources.append(tier0)
    tier1 = []

    # Number of threads for second layer (tier1)
    t1_num_threads = 4
    wait = 0

    # Create a size based on length of links found
    chunksize = int((len(res0.links_found))/t1_num_threads)
    threads = []

    # Pass in chunks of res0.links_found to threads to be processed
    for i in range(t1_num_threads):
        t = Thread(res0.links_found[chunksize*i:(chunksize*(i+1))], tier1, i, wait)
        threads.append(t)
        t.start()

    # Wait for all threads to finish
    # Tier1 should be populated with resources
    for t in threads:
        t.join()

    # process remaining links
    remains = []
    remaining = len(res0.links_found) % t1_num_threads
    rem = (len(res0.links_found) - remaining)
    for rem in range(len(res0.links_found)):
        remains.append(res0.links_found[rem])
    crawl(remains, tier1, wait)

    print("Length tier1: {}".format(len(tier1)))
    # To hold the links found in third layer
    tier2_links = []

    # Find links on the pages in tier1
    for r in tier1:
        r.find_links()
        if r.links_found is not None:
            tier2_links.extend(r.links_found)

    # Add tier1 to resources
    resources.append(tier1)
    tier2 = []

    # Queue for third layer processing
    q = queue.Queue()
    crawl_time = time.clock()
    print("Gathering data from pages...")

    # Create pool of threads, more threads since
    # third layer is larger, naturally
    # Pass queue instance and thread count
    wait = 30
    t2_num_threads = 10
    for j in range(t2_num_threads):
        thread = ThreadClass(q, j, wait)
        thread.setDaemon(True)
        thread.start()

    size = int((len(tier2_links))/t2_num_threads)
    # Populate queue with chunks of links
    # Will be passed into crawl
    for k in range(t2_num_threads):
        q.put((tier2_links[(size*k):(size*(k+1))], tier2))
    # TODO: fix 429 Too many requests

    # Wait until everything is processed
    q.join()
    resources.append(tier2)
    print('Finished crawl. {} process time'.format(time.clock() - crawl_time))
elif mode is 2:
    url_list = input("Enter a list of urls, each on a different line: ")
    for each in url_list:
        r = Resource(each)
        r.get_resource_data()
        resources.append(r)
else:
    re_prompt = input("Error: That integer is not an option. Please enter 1) to crawl from a single url or 2) to"
                      "scrape data from a list of urls")

for tier in resources:
    print(len(tier))

# <editor-fold desc="Write to excel">
write_time0 = time.clock()
if mode is 1:
    index = 0
    for tier in resources:
        if tier is not None and len(tier) > 0:
            ws = wb.create_sheet(index, str(index))
            make_headers(ws)
            for value in tier:
                row = ws.get_highest_row() + 1
                write_resource(ws, row, value)
        else:
            continue
        index += 1
elif mode is 2:
    index = 0
    ws = wb.create_sheet(index, str(index))
    make_headers(ws)
    row = ws.get_highest_row() + 1
    term_links = []
    for tier in resources:
        for item in tier:
            write_resource(ws, row, item)
            index += 1
else:
    print("Error in write processing")
    exit()

write_time = time.clock() - write_time0
print('Write time: {}'.format(write_time))
# </editor-fold>

print('broken links: {}'.format(brokenLinks))

wb.save(filename+".xlsx")