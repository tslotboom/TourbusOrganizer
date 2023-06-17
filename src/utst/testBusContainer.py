from ..BusContainer import BusContainer
from ..Tourist import Tourist

import unittest


class TestBus(unittest.TestCase):

    def testInit(self):
        bus = BusContainer(0)
        self.assertEqual(bus.bus, [])
        bus = BusContainer(1)
        self.assertEqual(bus.bus, [[None, None]])
        bus = BusContainer(2)
        self.assertEqual(bus.bus, [[None, None]])
        bus = BusContainer(3)
        self.assertEqual(bus.bus,
                         [[None, None],
                          [None, None]])
        bus = BusContainer(4)
        self.assertEqual(bus.bus,
                         [[None, None],
                          [None, None]])
        bus = BusContainer(7)
        self.assertEqual(bus.bus,
                         [[None, None],
                          [None, None],
                          [None, None],
                          [None, None]])
        bus = BusContainer(14)
        self.assertEqual(bus.bus,
                         [[None, None],
                          [None, None],
                          [None, None],
                          [None, None],
                          [None, None],
                          [None, None],
                          [None, None]])

    def testSetAndGetSeat(self):
        bus = BusContainer(2)
        tourist = Tourist('bob')
        seatNum = 1
        bus.add(tourist, seatNum)
        self.assertEqual(bus.get(1), tourist)
        self.assertEqual(bus.get(0), None)
        self.assertTrue(seatNum in tourist.seatPositions)

    def testSetSeatException(self):
        bus = BusContainer(2)
        tourist = Tourist('bob')
        with self.assertRaises(RuntimeError):
            bus.add(tourist, 1000)

    def testGetSeatException(self):
        bus = BusContainer(2)
        tourist = Tourist('bob')
        bus.add(tourist, 0)
        with self.assertRaises(RuntimeError):
            bus.get(2)

    def testYieldSeats(self):
        bus = BusContainer(4)
        tourists = [Tourist(str(i)) for i in range(0, 4)]
        for i in range(len(tourists)):
            bus.add(tourists[i], i)
        count = 0
        for seat in bus.yieldSeats():
            self.assertEqual(seat, tourists[count])
            count += 1

    def testSeatIsEmpty(self):
        bus = BusContainer(4)
        bus.add(Tourist('bob'), 0)
        bus.add(Tourist('bob'), 1)
        self.assertFalse(bus.seatIsEmpty(0))
        self.assertFalse(bus.seatIsEmpty(1))
        self.assertTrue(bus.seatIsEmpty(2))
        self.assertTrue(bus.seatIsEmpty(3))

    def testGetAdjacentSeat(self):
        bus = BusContainer(4)
        self.assertEqual(bus.adjacentSeat(0), 1)
        self.assertEqual(bus.adjacentSeat(1), 0)
        self.assertEqual(bus.adjacentSeat(2), 3)
        self.assertEqual(bus.adjacentSeat(3), 2)

