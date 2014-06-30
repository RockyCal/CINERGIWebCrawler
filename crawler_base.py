from bs4 import BeautifulSoup
import requests

#Function printTitles prints all the titles of the links on a given site
def printTitles(url):
    asOfVisited = []

    HTTP = 'http://'

    r = requests.get(url)
    htmlText = r.text
    soup = BeautifulSoup(htmlText)

    for tag in soup.findAll('a', href=True): # filters out the a tag so we can access the right section of HTML
        if HTTP in tag['href']:
            asOfVisited.append(tag)
    for each in asOfVisited:
        print(each.text)
    return asOfVisited

HTTP = 'http://'
url = "http://www.greenseas.eu/content/standards-and-related-web-information"

urls = [url]  # stack of urls to scrape
visited = [url]  # urls visited

while len(urls) > 0:
    try:
        r = requests.get(urls[0])
        htmlText = r.text
    except requests.Timeout:
        print('{}: Timeout error'.format(url[0]))
    except requests.ConnectionError:
        print('{}: Connection error'.format(url[0]))
    except requests.TooManyRedirects:
        print('{}: Too Many Redirects'.format(url[0]))
    except requests.HTTPError:
        print('{}: HTTP Error'.format(url[0]))

    soup = BeautifulSoup(htmlText)
    urls.pop(0)

for tag in soup.findAll('a', href=True):
        if HTTP in tag['href'] and tag['href'] not in visited:
            urls.append(tag['href'])
            visited.append(tag['href'])

firstRun = printTitles(url)

#Follows the links and crawls the sub-sites
for each in visited:
    print(each)
    secondRun = printTitles(each)
