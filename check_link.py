import requests
from crawler_base import brokenLinks
from urllib.request import urlopen
from urllib.error import URLError
import tldextract

def check_type(url):
    url_front = url[:url.index(':')]
    if url_front == "http" or url_front == "https":
        return "HTTP"
    elif url_front == "ftp":
        return "FTP"
    else:
        return " "

"""
Name: check_link.py()
Params: url - link to check
Purpose: Make sure links work and go somewhere
Returns: 1 if link works w/o error
         Exits if link is broken
"""

def check_link(url):
    # works = 1
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

def check_again(new_url):
    try:
        rq = requests.get(new_url)
        cq = rq.status_code
    except requests.ConnectionError:
        #fixed = 0
        print('{}: Connection error'.format(new_url))
        brokenLinks.append(new_url)
        return " "
    except requests.Timeout:
        #fixed = 0
        print('{}: Timeout error'.format(new_url))
        brokenLinks.append(new_url)
        return " "
    except requests.TooManyRedirects:
        #fixed = 0
        print('{}: Too Many Redirects'.format(new_url))
        brokenLinks.append(new_url)
        return " "
    except requests.HTTPError:
        #fixed = 0
        print('{}: HTTP Error'.format(new_url))
        brokenLinks.append(new_url)
        return " "
    else:
        if cq != 200:
            #fixed = 0
            print('{}: Error code {}'.format(new_url, cq))
            brokenLinks.append(new_url)
            return " "
    return new_url