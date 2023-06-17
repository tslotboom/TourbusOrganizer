from ..Tourist import Tourist

import unittest


class TestTourist(unittest.TestCase):

    def testCalculateTotalSeatScore(self):
        tourist = Tourist('a')
        self.assertEqual(tourist.calculateTotalSeatScore(), 0)
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
        self.assertAlmostEqual(tourist.calculateTotalSeatScore(), 14)

    def testTouristAlreadySatInRow(self):
        seatNum = 1
        tourist = Tourist('bob')
        tourist.seatPositions.append(seatNum)
        self.assertTrue(tourist.alreadySatInRow(seatNum))
        self.assertTrue(tourist.alreadySatInRow(0))
        self.assertFalse(tourist.alreadySatInRow(2))

    def testInGroup(self):
        tourist = Tourist('bob')
        self.assertFalse(tourist.inGroup())
        tourist.groupID = 2
        self.assertTrue(tourist.inGroup())
