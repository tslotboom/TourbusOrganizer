from ..BusHelper import BusHelper

import unittest


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