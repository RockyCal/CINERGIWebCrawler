import threading
class Thread(threading.Thread):
    def __init__(self, url_queue, content_queue):
        self.c_queue = content_queue
        self.u_queue = url_queue
        super(Thread, self).__init__()
    def run(self):
        while True:
            next_url = self.u_queue.get()
            #data = requests.get(next_url)
            while self.c_queue.full():
                pass
            self.c_queue.put(data)
            self.u_queue.task_done()