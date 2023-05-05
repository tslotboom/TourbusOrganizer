import unittest
from ..Tourbus import Tourist, Tourbus


class TestTourist(unittest.TestCase):

    def testCalculateSeatScoreException(self):
        tourist = Tourist('a')
        with self.assertRaises(RuntimeError):
            tourist.calculateSeatScore()

    def testCalculateSeatScore(self):
        tourist = Tourist('a')
        tourist.seatPositions = [0]
        self.assertEqual(tourist.calculateSeatScore(), 0)
        tourist.seatPositions = [1]
        self.assertEqual(tourist.calculateSeatScore(), 0)
        tourist.seatPositions = [2]
        self.assertEqual(tourist.calculateSeatScore(), 1)
        tourist.seatPositions = [3]
        self.assertEqual(tourist.calculateSeatScore(), 1)
        tourist.seatPositions = [1, 1]
        self.assertEqual(tourist.calculateSeatScore(), 0)
        tourist.seatPositions = [1, 8, 2, 5, 3, 12]
        self.assertAlmostEqual(tourist.calculateSeatScore(), 2.3333333333)


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
            # Tourist('i'),
            # Tourist('j'),
            # Tourist('k'),
            # Tourist('l'),
            # Tourist('m'),
            # Tourist('n'),
        ]
        return Tourbus(tourists)

    def testFillSeats(self):
        tourbus = self.getTourbus()
        tourbus.fillSeatsForTrip()

    def testReorderTouristList(self):
        tourbus = self.getTourbus()
        tourbus.fillSeatsForTrip()
        tourbus.reorderTouristList()
        # for tourist

