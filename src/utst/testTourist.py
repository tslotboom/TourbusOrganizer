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

    def testSitDown(self):
        tourist = Tourist("bob")
        seatNum = 3
        tourist.sitDown(seatNum)
        self.assertEqual(tourist.seatPositions[0], seatNum)
        self.assertEqual(tourist.rightSeatings, 1)
        self.assertEqual(tourist.leftSeatings, 0)
        self.assertEqual(tourist.totalSeatScore, 1)

        seatNum = 2
        tourist.sitDown(seatNum)
        self.assertEqual(tourist.seatPositions[1], seatNum),
        self.assertEqual(tourist.rightSeatings, 1)
        self.assertEqual(tourist.leftSeatings, 1)
        self.assertEqual(tourist.totalSeatScore, 2)

    def testRemoveSeat(self):
        tourist = Tourist("bob")
        self.assertEqual(len(tourist.seatPositions), 0)
        self.assertEqual(tourist.rightSeatings, 0)
        self.assertEqual(tourist.leftSeatings, 0)
        self.assertEqual(tourist.totalSeatScore, 0)

        tourist.removeSeat()
        self.assertEqual(len(tourist.seatPositions), 0)
        self.assertEqual(tourist.rightSeatings, 0)
        self.assertEqual(tourist.leftSeatings, 0)
        self.assertEqual(tourist.totalSeatScore, 0)

        tourist.sitDown(1)
        tourist.removeSeat()
        self.assertEqual(len(tourist.seatPositions), 0)
        self.assertEqual(tourist.rightSeatings, 0)
        self.assertEqual(tourist.leftSeatings, 0)
        self.assertEqual(tourist.totalSeatScore, 0)

        tourist.sitDown(3)
        tourist.sitDown(3)
        tourist.sitDown(4)
        tourist.sitDown(4)

        tourist.removeSeat()
        self.assertEqual(len(tourist.seatPositions), 3)
        self.assertEqual(tourist.rightSeatings, 2)
        self.assertEqual(tourist.leftSeatings, 1)
        self.assertEqual(tourist.totalSeatScore, 4)