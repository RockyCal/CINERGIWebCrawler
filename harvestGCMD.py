__author__ = 'Raquel'

import xml.etree.ElementTree as eTree
from urllib.request import urlopen

# Concept schemes to ignore due to mostly internal usage by NASA or too broad to be helpful
toIgnore = ['horizontalresolutionrange', 'locations', 'temporalresolutionrange' 'verticalresolutionrange']
tree = eTree.parse(urlopen('http://gcmdservices.gsfc.nasa.gov/static/kms/concepts/concepts.xml'))
root = tree.getroot()

corpus = open('crawler_corpus.txt', 'w+')

for concept in root.findall('conceptBrief'):
    if concept.get('conceptScheme') is 'Trash':
        continue
    if concept.get('conceptScheme').isupper():
        corpus.write(concept.get('prefLabel'))
    else:
        corpus.write('--------------------------------------------------------\n')
        corpus.write(concept.get('prefLabel')+'\n')


corpus.close()