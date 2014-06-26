import threading
class Thread(threading.Thread):
    def __init__(self, content_queue, url_queue):
        self.c_queue = content_queue
        self.u_queue = url_queue
        super(Thread, self).__init__()
    def run(self):
        while True:
            data = self.c_queue.get()
            #process data
            for link in links:
                self.u_queue.put(link)
            self.c_queue.task_done()