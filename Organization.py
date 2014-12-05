__author__ = 'Raquel'

import xml.etree.ElementTree as ET
from urllib.request import urlopen
import urllib.parse
import re

# VIAF base url
viaf_base = 'http://viaf.org/viaf/search'

# string for searching corporate names
corporate_names = 'local.corporateNames'

# String for searching all of viaf
all_viaf = 'all'


class Organization:
    def __init__(self, name):
        self.name = name
        self.string = '{}'.format(name)
    link = ''
    uri = ''
    validated = False

    def validate_in_viaf(self):
        to_encode = self.string
        encoded_search_terms = pseudo_encode(to_encode)
        terms = [corporate_names, all_viaf, encoded_search_terms]
        query_string = 'query='
        for each in terms:
            query_string += each
            if each is not terms[len(terms)-1]:
                query_string += '+'
        data = {'recordSchema': 'BriefVIAF',
                'sortKeys': 'holdingscount'}
        values = urllib.parse.urlencode(data, 'utf-8')
        full_url = viaf_base + '?' + query_string + '&' + values
        self.link = full_url
        tree = ET.parse(urlopen(full_url))
        root = tree.getroot()
        records = root.find('{http://www.loc.gov/zing/srw/}records')
        if records is None:
            return
        for child in records:
            record_data = child.find('{http://www.loc.gov/zing/srw/}recordData')
            cluster = record_data.find('{http://viaf.org/viaf/terms#}VIAFCluster')
            ctitle = cluster.find('{http://viaf.org/viaf/terms#}mainHeadings').find('{http://viaf.org/viaf/terms#}data').\
                find('{http://viaf.org/viaf/terms#}text')
            # Find a generic match
            if re.search(u'{0:s} \(.*\)$'.format(self.string), str(ctitle.text)) is not None:
                viaf_id = cluster.find('{http://viaf.org/viaf/terms#}viafID')
                if viaf_id is not None:
                    self.uri = viaf_id.text
                    self.validated = True


def already_in(string, orgs):
    for o in orgs:
        if o.name == string:
            return True
    return False


def pseudo_encode(string):
    string_to_encode = '"' + string + '"'
    return re.sub('\s', '%2B', string_to_encode)

