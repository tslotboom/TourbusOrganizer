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

    def testColorPicker(self):
        self.assertEqual(colorPicker(0, 6), "00ff7f7f")
        self.assertEqual(colorPicker(1, 6), "00ffff7f")
        self.assertEqual(colorPicker(2, 6), "007fff7f")
        self.assertEqual(colorPicker(3, 6), "007fffff")
        self.assertEqual(colorPicker(4, 6), "007f7fff")
        self.assertEqual(colorPicker(5, 6), "00ff7fff")
        self.assertEqual(colorPicker(6, 6), "00ff7f7f")
