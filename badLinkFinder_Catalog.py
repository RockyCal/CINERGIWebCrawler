__author__ = 'Raquel'
# Go through HLI and ensure all links work


from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.parse import urljoin
from check_link import check_link

LAST_PG = 55

base_url = 'http://hydro10.sdsc.edu/'

start_url = 'http://hydro10.sdsc.edu/HLIResources/Resources'

soup = BeautifulSoup(urlopen(start_url).read())
current_page = soup.find('div', {'class': 'pagination'}).find('li', {'class': 'active'})
page_num = current_page.find('a').text
find_next = current_page.find_next('li')
next_page = find_next.find('a')

while current_page.find_next('li') is not None:
    # Get the table
    table = soup.find('table')

    # Get all rows in the table
    table_rows = table.find_all('tr')

    # Pop off header row
    table_rows.pop(0)

    # Each row in the table is a resource
    for a_resource in table_rows:
        title = a_resource.find('td', {'class': 'resTitle'}).find('div').text
        short_title = (title[:50] + '..') if len(title) > 50 else title
        link_tag = a_resource.find('a', href=True, text='Link')
        if link_tag is not None:
            status = check_link(link_tag['href'])
            if status is not "working":
                print('PAGE {}. {} : {}'.format(page_num, short_title, status))

    next_page = current_page.find_next('li').find('a')
    full_url = urljoin(base_url, next_page['href'])
    soup = BeautifulSoup(urlopen(full_url).read())
    current_page = soup.find('div', {'class': 'pagination'}).find('li', {'class': 'active'})
    page_num = current_page.find('a').text