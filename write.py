__author__ = 'Raquel'
from term_links import find_term_links

def write_resource(ws, row_num, resource):
    term_links = []
    ws['A%s' % row_num].value = resource.title
    ws['C%s' % row_num].value = resource.link
    term_links.append('URL Type: http://cinergiterms.weebly.com/url-type.html')
    ws['D%s' % row_num].value = resource.org
    ws['E%s' % row_num].value = ', '.join(sorted(resource.themes))
    term_links.append(find_term_links(resource.themes))
    ws['F%s' % row_num].value = ', '.join(sorted(resource.resource_type))

    term_links.append(find_term_links(resource.resource_type))
    #ws['G%s' % row_num].value = resource.url_type
    #ws['H%s' % row_num].value = resource.tld
    term_links.append('TLD: http://cinergiterms.weebly.com/top-level-domain.html')
    #ws['I%s' % row_num].value = resource.country_code
    term_links.append('Country Code: http://cinergiterms.weebly.com/country-codes.html')
    ws['J%s' % row_num].value = resource.social_media
    ws['K%s' % row_num].value = str(term_links)