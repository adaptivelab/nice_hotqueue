import unittest
import fudge
from nice_hotqueue import NiceHotQueue


class FakeBaseQueue(object):

    @property
    def name(self):
        return 'nicey'

    @property
    def _HotQueue__redis(self):
        return fudge.Fake('_HotQueue__redis').has_attr(
            connection_pool=fudge.Fake('connection_pool').has_attr(
                _available_connections=[
                    fudge.Fake('conn').has_attr(host='127.0.0.1')
                ]
            )
        )


class FakeFullQueue(FakeBaseQueue):

    def __init__(self):
        self.size = 10002

    def __len__(self):
        self.size -= 1
        return self.size


class FakeStaysFullQueue(FakeBaseQueue):

    def __init__(self):
        self.size = 10001

    def __len__(self):
        return self.size


class FakeEmptyQueue(FakeBaseQueue):

    def __len__(self):
        return 0


class FakeSmallQueue(FakeBaseQueue):

    def __init__(self):
        self.size = 4

    def __len__(self):
        self.size -= 1
        return self.size


class TestNiceHotQueue(unittest.TestCase):

    @fudge.patch('nice_hotqueue.logger')
    def test_queue_only_logs_once_when_backing_off(self, logger):
        (logger
            .expects('info')
            .with_args(
                'backing off hotqueue:nicey on '
                '127.0.0.1 (queue size: 10001)')
            .next_call()
            .with_args(
                'inserting into hotqueue:nicey on '
                '127.0.0.1 again (queue size: 10001)')
        )
        fake_queue = FakeStaysFullQueue()
        fake_queue.put = fudge.Fake('put').is_callable().expects_call()

        queue = NiceHotQueue(fake_queue)
        queue.backOffABit = (
            fudge.Fake('backOffABit')
                .is_callable()
                .expects_call()
                .times_called(3)
            )
        queue.queueIsTooFull = (
            fudge.Fake('queueIsTooFull')
                .is_callable()
                .returns(True)
                .next_call()
                .returns(True)
                .next_call()
                .returns(True)
                .next_call()
                .returns(False))
        queue.put('something')


    @fudge.test
    def test_queue_name_and_hosts(self):
        fake_queue = FakeSmallQueue()
        queue = NiceHotQueue(fake_queue)
        self.assertEqual(
            queue.queue_name_and_hosts,
            'hotqueue:nicey on 127.0.0.1'
        )

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

