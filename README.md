CINERGIWebCrawler
=================

This crawler/scraper is meant to gather metadata from earth science resources.

Dependencies are Python 3.4
The following libraries are used in the code:
xml.etree.ElementTree, urllib.request, urllib.parse, re and bs4

Please install urllib3, beautifulsoup4, and tldextract by running the following commands:

$ python -m pip install urllib3       (in c:\python34)

$ python -m pip install beautifulsoup4

$ python -m pip install tldextract

To run the crawler:
git clone https://github.com/RockyCal/CINERGIWebCrawler.git
cd CINERGIWebCrawler
python3.4 crawler_base.py

Prompt will appear,

$ Enter url to crawl:

Enter a valid url to crawl for organization, resource type,  discipline (field of science) and contact info
Organization will be checked against Virtual International Authority File and if validated, the field will read true
