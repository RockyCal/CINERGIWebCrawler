from bs4 import BeautifulSoup
import requests

url = "http://www.greenseas.eu/content/standards-and-related-web-information"

urls = [url]  # stack of urls to scrape
visited = [url]  #urls visited

while len(urls) > 0:
    try:
        r = requests.get(urls[0])
        htmlText = r.text
    except TimeoutError:
        print('{}: Timeout error'.format(url[0]))
    soup = BeautifulSoup(htmlText)
    urls.pop(0)

for tag in soup.findAll('a', href=True):
    print(tag)
    print("Raquel")