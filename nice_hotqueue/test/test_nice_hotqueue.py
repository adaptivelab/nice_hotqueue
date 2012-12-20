import unittest
import fudge
from nice_hotqueue import NiceHotQueue


class FakeFullQueue(object):

    def __init__(self):
        self.size = 10002

    def __len__(self):
        self.size -= 1
        return self.size


class FakeEmptyQueue(object):

    def __len__(self):
        return 0


class FakeSmallQueue(object):

    def __init__(self):
        self.size = 3

    def __len__(self):
        self.size -= 1
        return self.size


class TestNiceHotQueue(unittest.TestCase):

    @fudge.test
    def test_put_sleeps_if_the_queue_is_too_full(self):
        fake_queue = FakeFullQueue()
        fake_queue.put = fudge.Fake('put').is_callable().expects_call()

        queue = NiceHotQueue(fake_queue)
        queue.backOffABit = fudge.Fake('backOffABit').is_callable().expects_call().times_called(1)
        queue.put("something")

    @fudge.test
    def test_put_doesnt_sleep_if_the_queue_is_empty(self):
        fake_queue = FakeEmptyQueue()
        fake_queue.put = fudge.Fake('put').is_callable().expects_call()

        queue = NiceHotQueue(fake_queue)
        queue.backOffABit = fudge.Fake('backOffABit')
        queue.put("something")

    @fudge.test
    def test_smaller_queue(self):
        fake_queue = FakeSmallQueue()
        fake_queue.put = fudge.Fake('put').is_callable().expects_call()

        queue = NiceHotQueue(fake_queue, max_queue_size=1)
        queue.backOffABit = fudge.Fake('backOffABit').is_callable().expects_call().times_called(1)
        queue.put("something")

    @fudge.patch('nice_hotqueue.time')
    def test_back_off_a_bit(self, FakeTime):
        FakeTime.expects('sleep').with_args(3)
        self.test_put_sleeps_if_the_queue_is_too_full()

