import unittest
from ..Tourbus import BusHelper, Tourist, Tourbus, BusContainer


class TestBusHelper(unittest.TestCase):

    def testGetRowAndColumn(self):
        busHelper = BusHelper()
        row, col = busHelper.getRowAndCol(0)
        self.assertEqual(row, 0)
        self.assertEqual(col, 0)
        row, col = busHelper.getRowAndCol(1)
        self.assertEqual(row, 0)
        self.assertEqual(col, 1)
        row, col = busHelper.getRowAndCol(2)
        self.assertEqual(row, 1)
        self.assertEqual(col, 0)
        row, col = busHelper.getRowAndCol(3)
        self.assertEqual(row, 1)
        self.assertEqual(col, 1)
        row, col = busHelper.getRowAndCol(8)
        self.assertEqual(row, 4)
        self.assertEqual(col, 0)

    def testCalculateSeatScore(self):
        busHelper = BusHelper()
        self.assertEqual(busHelper.calculateSeatScore(0), 0)
        self.assertEqual(busHelper.calculateSeatScore(1), 0)
        self.assertEqual(busHelper.calculateSeatScore(2), 1)
        self.assertEqual(busHelper.calculateSeatScore(3), 1)
        self.assertEqual(busHelper.calculateSeatScore(4), 2)
        self.assertEqual(busHelper.calculateSeatScore(5), 2)
        self.assertEqual(busHelper.calculateSeatScore(6), 3)
        self.assertEqual(busHelper.calculateSeatScore(7), 3)





class TestTourist(unittest.TestCase):

    def testCalculateSeatScoreException(self):
        tourist = Tourist('a')
        with self.assertRaises(RuntimeError):
            tourist.calculateTotalSeatScore()

    def testCalculateSeatScore(self):
        tourist = Tourist('a')
        tourist.seatPositions = [0]
        self.assertEqual(tourist.calculateTotalSeatScore(), 0)
        tourist.seatPositions = [1]
        self.assertEqual(tourist.calculateTotalSeatScore(), 0)
        tourist.seatPositions = [2]
        self.assertEqual(tourist.calculateTotalSeatScore(), 1)
        tourist.seatPositions = [3]
        self.assertEqual(tourist.calculateTotalSeatScore(), 1)
        tourist.seatPositions = [1, 1]
        self.assertEqual(tourist.calculateTotalSeatScore(), 0)
        tourist.seatPositions = [1, 8, 2, 5, 3, 12]
        self.assertAlmostEqual(tourist.calculateTotalSeatScore(), 2.3333333333)

    def testTouristAlreadySatInRow(self):
        seatNum = 1
        tourist = Tourist('bob')
        tourist.seatPositions.append(seatNum)
        self.assertTrue(tourist.alreadySatInRow(seatNum))
        self.assertFalse(tourist.alreadySatInRow(0))


class TestTourbus(unittest.TestCase):

    def getTourbus(self):
        tourists = [
            Tourist('a'),
            Tourist('b'),
            Tourist('c'),
            Tourist('d'),
            Tourist('e'),
            Tourist('f'),
            Tourist('g'),
            Tourist('h'),
            Tourist('i'),
            Tourist('j'),
            Tourist('k'),
            Tourist('l'),
            Tourist('m'),
            Tourist('n'),
        ]
        return Tourbus(tourists, 4)

    def testConstructorError1(self):
        with self.assertRaises(RuntimeError):
            Tourbus([], 1)

    def testConstructorError2(self):
        with self.assertRaises(RuntimeError):
            Tourbus([Tourist('bob')], 0)

    def testConstructorError3(self):
        with self.assertRaises(RuntimeError):
            Tourbus([Tourist('bob')], 0)

    def testGetProjectedSeatScore(self):
        tourbus = self.getTourbus()
        self.assertEqual(tourbus.getProjectedSeatScore(1, 1), 0)
        self.assertEqual(tourbus.getProjectedSeatScore(1, 10), 0)
        self.assertEqual(tourbus.getProjectedSeatScore(10, 1), 2)
        self.assertEqual(tourbus.getProjectedSeatScore(10, 2), 4)
        self.assertEqual(tourbus.getProjectedSeatScore(10, 3), 6)
        self.assertEqual(tourbus.getProjectedSeatScore(10, 4), 8)
        self.assertEqual(tourbus.getProjectedSeatScore(10, 5), 10)
        self.assertEqual(tourbus.getProjectedSeatScore(8, 1), 1.5)
        self.assertEqual(tourbus.getProjectedSeatScore(8, 2), 3)
        self.assertEqual(tourbus.getProjectedSeatScore(8, 3), 4.5)
        self.assertEqual(tourbus.getProjectedSeatScore(8, 4), 6)
        self.assertEqual(tourbus.getProjectedSeatScore(14, 3), 9)

    def testGetAvailableScores(self):
        bob = Tourist("bob")
        bob.seatPositions = [2]
        joe = Tourist("joe")
        john = Tourist("john")
        tourbus = Tourbus([bob, joe, john], 2)
        availableSeatScores = tourbus.getAvailableSeatScores(bob)
        self.assertEqual(availableSeatScores, [0])

    def testGetAllowedRepeats



    # def testFillSeats(self):
    #     tourbus = self.getTourbus()
    #     tourbus.fillSeatsForTrip()
    #
    # def testReorderTouristList(self):
    #     tourbus = self.getTourbus()
    #     tourbus.fillSeatsForTrip()
    #     tourbus.reorderTouristList()
    #     # for tourist


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

