from Resource import Resource
import csv


# <editor-fold desc="Protocol constants">
HTTP = 'http://'
preFTP = 'ftp://'
# </editor-fold>

"""
Program begins.
"""
# Total visited links
visited = []
# Total working links found
urls = []

resources = []


# Create excel file
# wb = Workbook()
# filename = input("Enter a title for the excel file: ")
url = input("Enter url to crawl: ")

resource = Resource(url)
resource.get_resource_data()
resource_values = {'title': resource.title, 'url': resource.link, 'link status': resource.status,
                   'resource types': resource.resource_type, 'disciplines': resource.themes,
                   'organization': resource.get_org(), 'organization validated in VIAF': resource.org.validated,
                   'VIAF uri': resource.org.uri, 'contact organization': resource.resource_contact_org,
                   'contact name': resource.resource_contact_person_name,
                   'contact email': resource.resource_contact_email, 'contact phone': resource.resource_contact_phone}

fieldnames = ['title', 'url', 'link status', 'resource types', 'disciplines', 'organization',
              'organization validated in VIAF', 'VIAF uri', 'contact organization', 'contact name', 'contact email',
              'contact phone']

with open('{}.csv'.format(resource.title), 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerow(resource_values)

# <editor-fold desc="Write to excel">
"""
write_time0 = time.clock()
index = 0
ws = wb.create_sheet(index, str(index))
make_headers(ws)
row = ws.get_highest_row() + 1
term_links = []
for tier in resources:
    for item in tier:
        write_resource(ws, row, item)
        row += 1
    index += 1
    row = 1
    ws = wb.create_sheet(index, str(index))

write_time = time.clock() - write_time0
print('Write time: {}'.format(write_time))
wb.save(filename+".xlsx")
"""
# </editor-fold>
