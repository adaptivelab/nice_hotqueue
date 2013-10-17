import logging
import time

logger = logging.getLogger('nice_hotqueue')
# use NullHandler as default to avoid output if no logging config
# in application using library
logger.addHandler(logging.NullHandler())


class NiceHotQueue(object):
    """
    Wrapper around a hotqueue that doesn't let it put if the queue is too full.
    """

    def __init__(self, queue, max_queue_size=10000):
        self.queue = queue
        self.max_queue_size = max_queue_size
        self.backing_off = False

    @property
    def redis_hosts(self):
        hosts = []
        pool = (self._HotQueue__redis.
            connection_pool._available_connections)
        for conn in pool:
            # might be a socket connection without a host
            try:
                hosts.append(conn.host)
            except AttributeError:
                hosts.append(None)
        return hosts

    @property
    def queue_name_and_hosts(self):
        return 'hotqueue:{} on {}'.format(
            self.queue.name, ','.join(self.redis_hosts))

    def put(self, *args):
        while self.queueIsTooFull():
            if not self.backing_off:
                msg = 'backing off {} (queue size: {})'.format(
                    self.queue_name_and_hosts, len(self.queue))
                logger.info(msg)
                self.backing_off = True
            self.backOffABit()

        if self.backing_off:
            msg = 'inserting into {} again (queue size: {})'.format(
                self.queue_name_and_hosts, len(self.queue))
            logger.info(msg)
            self.backing_off = False

        self.queue.put(*args)

    def queueIsTooFull(self):
        return len(self.queue) > self.max_queue_size

    def backOffABit(self):
        """Sleep for 3 seconds."""
        time.sleep(3)

    @property
    def _HotQueue__redis(self):
        """Mimic a HotQueue internally."""
        return self.queue._HotQueue__redis
