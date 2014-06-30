from bs4 import BeautifulSoup
import requests

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

print (visited)