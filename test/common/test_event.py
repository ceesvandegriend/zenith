import unittest
from dataclasses import dataclass

from zenith.common.event import append_listener, clear_listeners, fire_listeners, listeners


@dataclass
class Dummy():
    fired: int = 0


class DummyListener():
    def fire(self, dummy: Dummy):
        """

        :type dummy: object
        """
        dummy.fired = dummy.fired + 1


class TestEvent(unittest.TestCase):
    def setUp(self) -> None:
        ''' Remove registed listeners '''
        clear_listeners()

    def test_register_01(self) -> None:
        ''' Register 1 listener '''
        listener0 = DummyListener()
        append_listener('dummy', listener0)

        self.assertEqual(1, len(listeners('dummy')))
        self.assertEqual(listener0, listeners('dummy')[0])

    def test_register_02(self) -> None:
        ''' Register 2 listeners '''
        listener0 = DummyListener()
        listener1 = DummyListener()
        append_listener('dummy', listener0)
        append_listener('dummy', listener1)

        self.assertEqual(2, len(listeners('dummy')))
        self.assertEqual(listener0, listeners('dummy')[0])
        self.assertEqual(listener1, listeners('dummy')[1])

    def test_register_03(self) -> None:
        ''' Register 3 listeners '''
        listener0 = DummyListener()
        listener1 = DummyListener()
        listener2 = DummyListener()
        append_listener('dummy', listener0)
        append_listener('dummy', listener1)
        append_listener('dummy', listener2)

        self.assertEqual(3, len(listeners('dummy')))
        self.assertEqual(listener0, listeners('dummy')[0])
        self.assertEqual(listener1, listeners('dummy')[1])
        self.assertEqual(listener2, listeners('dummy')[2])

    def test_fire_01(self) -> None:
        ''' Fire 1 listener '''
        append_listener('dummy', DummyListener().fire)
        data = Dummy()
        self.assertEqual(0, data.fired)
        fire_listeners('dummy', data)
        self.assertEqual(1, data.fired)

    def test_fire_02(self) -> None:
        ''' Fire 2 listeners '''
        append_listener('dummy', DummyListener().fire)
        append_listener('dummy', DummyListener().fire)
        data = Dummy()
        self.assertEqual(0, data.fired)
        fire_listeners('dummy', data)
        self.assertEqual(2, data.fired)

    def test_fire_03(self) -> None:
        ''' Fire 3 listeners '''
        append_listener('dummy', DummyListener().fire)
        append_listener('dummy', DummyListener().fire)
        append_listener('dummy', DummyListener().fire)
        data = Dummy()
        self.assertEqual(0, data.fired)
        fire_listeners('dummy', data)
        self.assertEqual(3, data.fired)

    def test_fire_04(self) -> None:
        ''' Fire 3 + 4 listeners '''
        append_listener('dummy0', DummyListener().fire)
        append_listener('dummy0', DummyListener().fire)
        append_listener('dummy0', DummyListener().fire)
        append_listener('dummy1', DummyListener().fire)
        append_listener('dummy1', DummyListener().fire)
        append_listener('dummy1', DummyListener().fire)
        append_listener('dummy1', DummyListener().fire)
        data0 = Dummy()
        data1 = Dummy()
        self.assertEqual(0, data0.fired)
        self.assertEqual(0, data1.fired)
        fire_listeners('dummy0', data0)
        fire_listeners('dummy1', data1)
        self.assertEqual(3, data0.fired)
        self.assertEqual(4, data1.fired)
