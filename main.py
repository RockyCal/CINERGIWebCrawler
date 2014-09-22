__author__ = 'Raquel'
# Go through HLI and ensure all links work


from bs4 import BeautifulSoup
from urllib.request import urlopen
from check_link import check_link

LAST_PG = 55

# TODO: Add full site capability (all 55 pages)

start_url = 'http://hydro10.sdsc.edu/HLIResources/Resources'

current_page = BeautifulSoup(urlopen(start_url).read())

# Get the table
table = current_page.find('table')

# Get all rows in the table
table_rows = table.find_all('tr')

# Pop off header row
table_rows.pop(0)

# Each row in the table is a resource
for a_resource in table_rows:
    title = a_resource.find('td', {'class': 'resTitle'}).find('div').text
    link_tag = a_resource.find('a', text='Link')
    status = check_link(link_tag['href'])
    if status is not "working":
        print('{}: {}'.format(title, status))