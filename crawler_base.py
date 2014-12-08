from Resource import Resource


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
#wb = Workbook()
#filename = input("Enter a title for the excel file: ")
url = input("Enter url to crawl: ")

resource = Resource(url)
resource.get_resource_data()
print("Resource url: " + resource.link)
print("Resource title: " + resource.title)
print("Resource link status: " + resource.status)
print("Resource types detected: " + resource.resource_type)
print("Resource disciplines: " + resource.themes)
print("Resource organization: " + resource.get_org())
print("Organization validated in VIAF: {}".format(resource.org.validated))
if resource.org.validated:
    print("Organization VIAF id: {} ".format(resource.org.uri))
print("Resource contact organization: " + resource.resource_contact_org)
print("Resource contact person name: " + resource.resource_contact_person_name)
print("Resource contact email: " + resource.resource_contact_email)
print("Resource contact phone: " + resource.resource_contact_phone)

# TODO: fix up accuracy of find_resource_types and find_disciplines
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
