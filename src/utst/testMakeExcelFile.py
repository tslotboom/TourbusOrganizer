import unittest
from ..MakeExcelFile import *


class TestMakeExcelFile(unittest.TestCase):

    def testGetExcelCol(self):
        self.assertEqual(getExcelCol(1), "A")
        self.assertEqual(getExcelCol(2), "B")
        self.assertEqual(getExcelCol(8), "H")
        self.assertEqual(getExcelCol(26), "Z")
        self.assertEqual(getExcelCol(27), "AA")
        self.assertEqual(getExcelCol(28), "AB")
        self.assertEqual(getExcelCol(29), "AC")
        self.assertEqual(getExcelCol(52), "AZ")
        self.assertEqual(getExcelCol(702), "ZZ")
        self.assertEqual(getExcelCol(703), "AAA")
        self.assertEqual(getExcelCol(10000), "NTP")
        self.assertEqual(getExcelCol(16384), "XFD")
