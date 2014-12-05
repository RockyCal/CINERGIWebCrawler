from urllib.request import urlopen
import threading
import time
from Resource import Resource


# <editor-fold desc="Protocol constants">
HTTP = 'http://'
preFTP = 'ftp://'
# </editor-fold>


class Thread(threading.Thread):
    def __init__(self, stack, tier, count, delay):
        threading.Thread.__init__(self)
        self.stack = stack
        self.tier = tier
        self.count = count
        self.delay = delay

    def run(self):
        crawl(self.stack, self.tier, self.delay)


class ThreadClass(threading.Thread):
    def __init__(self, que, count, delay):
        threading.Thread.__init__(self)
        self.queue = que
        self.count = count
        self.delay = delay

    def run(self):
        while True:
            items = self.queue.get()
            stack = items[0]
            new_tier = items[1]
            crawl(stack, new_tier, self.delay)
            self.queue.task_done()


"""
name: crawl
stack is stack of links
"""


def crawl(stack, new_tier, delay):
    while len(stack) > 0:
        # Make instance of Resource
        resource = Resource(stack.pop(0))
        if resource.status is "working":
            urlopen(resource.link)
            if resource.link not in visited:
                resource.get_resource_data()
                visited.append(resource.link)
                new_tier.append(resource)
        time.sleep(delay)

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
print(resource.link)
print(resource.title)
print(resource.status)
print(resource.resource_type)
print(resource.themes)
print(resource.get_org())
print(resource.org.validated)
if resource.org.validated:
    print(resource.org.uri)
print(resource.resource_contact_org)
print(resource.resource_contact_person_name)
print(resource.resource_contact_email)
print(resource.resource_contact_phone)

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
