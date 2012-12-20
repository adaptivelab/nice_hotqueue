import time


class NiceHotQueue(object):
    """
    Wrapper around a hotqueue that doesn't let it put if the queue is too full.
    """

    def __init__(self, queue, max_queue_size=10000):
        self.queue = queue
        self.max_queue_size = max_queue_size

    def put(self, *args):
        while self.queueIsTooFull():
            self.backOffABit()

        self.queue.put(*args)

    def queueIsTooFull(self):
        return len(self.queue) > self.max_queue_size

    def backOffABit(self):
        """Sleep for 3 seconds."""
        time.sleep(3)
