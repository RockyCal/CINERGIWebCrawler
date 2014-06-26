from breakdown import Parser, Grabber
from queue import Queue

num_threads = 4
max_size = 1000
url_queue = Queue()
content_queue = Queue(maxsize=max_size)

parsers = [Parser.Thread(content_queue, url_queue) for i in range(num_threads)]
grabbers = [Grabber.Thread(url_queue, content_queue) for i in range(num_threads)]

for thread in parsers+grabbers:
    thread.daemon = True
    thread.start()

url_queue.put('http://www.greenseas.eu/content/standards-and-related-web-information')