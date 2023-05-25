import unittest
from ..Tourbus import NeightbourClassification, BusHelper, Tourist, Tourbus, BusContainer
from typing import List


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
        self.assertFalse(tourist.alreadySatInRow(0))


class TestTourbus(unittest.TestCase):

    def getTourbus(self, numTourists, numDays):
        tourists = [Tourist(str(i)) for i in range(numTourists)]
        return Tourbus(tourists, numDays)

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
        tourbus = self.getTourbus(8, 3)
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
        self.helpTestGetAvailableScores(1, 1, [], [0])
        self.helpTestGetAvailableScores(3, 1, [], [0, 1])
        self.helpTestGetAvailableScores(8, 1, [], [0, 1, 2, 3])

        self.helpTestGetAvailableScores(3, 2, [2], [0])
        self.helpTestGetAvailableScores(8, 1, [0], [])
        self.helpTestGetAvailableScores(8, 3, [0, 7], [1, 2])
        self.helpTestGetAvailableScores(8, 4, [0, 7], [1, 2])
        self.helpTestGetAvailableScores(8, 5, [0, 7], [0, 1, 1, 2, 2, 3])
        self.helpTestGetAvailableScores(8, 5, [0, 1, 6, 7], [1, 1, 2, 2])

        self.helpTestGetAvailableScores(8, 8, [], [0, 0, 1, 1, 2, 2, 3, 3])
        self.helpTestGetAvailableScores(8, 8, [0, 0, 7], [1, 1, 2, 2, 3])
        self.helpTestGetAvailableScores(8, 16, [0, 0, 7], [0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3])
        self.helpTestGetAvailableScores(8, 16, [0, 1, 2, 3, 4, 5, 6, 7], [0, 0, 1, 1, 2, 2, 3, 3])
        self.helpTestGetAvailableScores(8, 16, [0, 1, 2, 3, 4, 5, 6, 7, 0, 1, 2], [1, 2, 2, 3, 3])
        self.helpTestGetAvailableScores(8, 16, [], [0] * 4 + [1] * 4 + [2] * 4 + [3] * 4)
        self.helpTestGetAvailableScores(16, 8, [], [0, 1, 2, 3, 4, 5, 6, 7])

    def helpTestGetAvailableScores(self, numTourists: int, numDays: int, seatPositions: List[int],
                                   expectedAvailableSeatScores: List[int]):
        tourbus = self.getTourbus(numTourists, numDays)
        tourist = tourbus.tourists[0]
        tourist.seatPositions = seatPositions
        availableSeatScores = tourbus.getAvailableSeatScores(tourist)
        self.assertCountEqual(availableSeatScores, expectedAvailableSeatScores)

    def testGetAllowedRepeats(self):
        self.helpTestGetAllowedRepeats(8, 1, 0)
        self.helpTestGetAllowedRepeats(8, 3, 0)
        self.helpTestGetAllowedRepeats(8, 4, 0)
        self.helpTestGetAllowedRepeats(8, 5, 1)
        self.helpTestGetAllowedRepeats(8, 6, 1)
        self.helpTestGetAllowedRepeats(8, 8, 1)
        self.helpTestGetAllowedRepeats(8, 9, 2)
        self.helpTestGetAllowedRepeats(1, 1, 0)
        self.helpTestGetAllowedRepeats(1, 2, 1)
        self.helpTestGetAllowedRepeats(1, 3, 2)
        self.helpTestGetAllowedRepeats(1, 4, 3)
        self.helpTestGetAllowedRepeats(1, 5, 4)
        self.helpTestGetAllowedRepeats(8, 14, 3)

    def helpTestGetAllowedRepeats(self, numTourists, numDays, expectedRowRepeats):
        tourbus = self.getTourbus(numTourists, numDays)
        self.assertEqual(tourbus.getAllowedRowRepeats(), expectedRowRepeats)

    def testGetAllowedSeatingsPerRow(self):
        self.helpTestGetAllowedSeatingsPerRow(4, 1, [0], [0, 1])
        self.helpTestGetAllowedSeatingsPerRow(8, 1, [0], [0, 1, 1, 1])
        self.helpTestGetAllowedSeatingsPerRow(8, 1, [], [1, 1, 1, 1])
        self.helpTestGetAllowedSeatingsPerRow(8, 8, [], [2, 2, 2, 2])

        self.helpTestGetAllowedSeatingsPerRow(8, 14, [], [4, 4, 4, 4])
        self.helpTestGetAllowedSeatingsPerRow(8, 15, [], [4, 4, 4, 4])
        self.helpTestGetAllowedSeatingsPerRow(8, 16, [], [4, 4, 4, 4])
        self.helpTestGetAllowedSeatingsPerRow(8, 17, [], [5, 5, 5, 5])

        self.helpTestGetAllowedSeatingsPerRow(8, 14, [0, 2], [3, 3, 4, 4])
        self.helpTestGetAllowedSeatingsPerRow(8, 14, [0, 2], [3, 3, 4, 4])
        self.helpTestGetAllowedSeatingsPerRow(8, 14, [0, 1, 2, 3], [2, 2, 4, 4])
        self.helpTestGetAllowedSeatingsPerRow(8, 14, [0, 0, 1, 1, 2, 2, 3, 3], [0, 0, 4, 4])
        self.helpTestGetAllowedSeatingsPerRow(8, 14, [7], [4, 4, 4, 3])

    def helpTestGetAllowedSeatingsPerRow(self, numTourists: int, numDays: int, touristSeatPositions: List[int],
                                         expectedAllowedSeatingsPerRow: List[int]):
        tourbus = self.getTourbus(numTourists, numDays)
        tourist = tourbus.tourists[0]
        tourist.seatPositions = touristSeatPositions
        allowedSeatingsPerRow = tourbus.getAllowedSeatingsPerRow(tourist)
        self.assertEqual(allowedSeatingsPerRow, expectedAllowedSeatingsPerRow)

    def testCheckIfSeatScoreIsFair(self):
        self.helpTestCheckIfSeatScoreIsFair(1, 1, [], 0, True)
        self.helpTestCheckIfSeatScoreIsFair(1, 1, [], 1, True)
        self.helpTestCheckIfSeatScoreIsFair(8, 1, [], 0, True)
        self.helpTestCheckIfSeatScoreIsFair(8, 8, [], 0, True)
        self.helpTestCheckIfSeatScoreIsFair(2, 2, [0], 0, True)

        self.helpTestCheckIfSeatScoreIsFair(8, 8, [7, 7, 7, 7], 7, False)
        self.helpTestCheckIfSeatScoreIsFair(8, 8, [7, 7, 7, 7], 5, False)
        self.helpTestCheckIfSeatScoreIsFair(8, 8, [7, 7, 7, 7], 3, False)
        self.helpTestCheckIfSeatScoreIsFair(8, 8, [7, 7, 7, 7], 1, True)

        self.helpTestCheckIfSeatScoreIsFair(8, 8, [0, 1, 2, 3, 4, 5, 6], 7, True)

        self.helpTestCheckIfSeatScoreIsFair(8, 8, [7, 6, 5, 4], 7, False)
        self.helpTestCheckIfSeatScoreIsFair(8, 8, [7, 6, 5, 4], 6, False)
        self.helpTestCheckIfSeatScoreIsFair(8, 8, [7, 6, 5, 4], 5, True)
        self.helpTestCheckIfSeatScoreIsFair(8, 8, [7, 6, 5, 4], 4, True)
        self.helpTestCheckIfSeatScoreIsFair(8, 8, [7, 6, 5, 4], 3, True)
        self.helpTestCheckIfSeatScoreIsFair(8, 8, [7, 6, 5, 4], 2, True)
        self.helpTestCheckIfSeatScoreIsFair(8, 8, [7, 6, 5, 4], 1, True)
        self.helpTestCheckIfSeatScoreIsFair(8, 8, [7, 6, 5, 4], 0, True)

    def helpTestCheckIfSeatScoreIsFair(self, numTourists: int, numDays: int, seatPositions: List[int], seat: int,
                                       expectedIsFair: bool):
        tourbus = self.getTourbus(numTourists, numDays)
        tourist = tourbus.tourists[0]
        tourist.seatPositions = seatPositions
        isFair = tourbus.seatScoreIsFair(tourist, seat)
        self.assertEqual(isFair, expectedIsFair)

    def testGetRemainingScoreAllowance(self):
        self.helpTestGetRemainingScoreAllowance(8, 8, [7, 6, 5, 4], 3)
        self.helpTestGetRemainingScoreAllowance(8, 8, [0, 1, 2, 3], 11)
        self.helpTestGetRemainingScoreAllowance(8, 8, [0, 0, 0, 0], 13)
        self.helpTestGetRemainingScoreAllowance(8, 8, [7, 7, 7, 7], 1)
        self.helpTestGetRemainingScoreAllowance(8, 8, [7, 7, 7, 7, 7], 0)

    def helpTestGetRemainingScoreAllowance(self, numTourists: int, numDays: int, seatPositions: List[int],
                                           expectedR: int):
        tourbus = self.getTourbus(numTourists, numDays)
        tourist = tourbus.tourists[0]
        tourist.seatPositions = seatPositions
        self.assertEqual(expectedR, tourbus.getRemainingScoreAllowance(tourist))

    def testGetOptimisticSumOfRemainingScores(self):
        self.helpTestGetOptimisticSumOfRemainingScores(8, 8, [7, 6, 5, 4], 2)
        self.helpTestGetOptimisticSumOfRemainingScores(8, 8, [0, 1, 2, 3], 10)
        self.helpTestGetOptimisticSumOfRemainingScores(8, 8, [7, 7, 7, 7], 2)
        self.helpTestGetOptimisticSumOfRemainingScores(8, 8, [0, 0, 0, 0], 6)

    def helpTestGetOptimisticSumOfRemainingScores(self, numTourists: int, numDays: int, seatPositions: List[int],
                                                  expectedO: int):
        tourbus = self.getTourbus(numTourists, numDays)
        tourist = tourbus.tourists[0]
        tourist.seatPositions = seatPositions
        self.assertEqual(expectedO, tourbus.getOptimisticSumOfRemainingScores(tourist))

    def testFillSeats(self):
        tourbus = self.getTourbus(8, 16)
        tourbus.fillSeatsForTrip2()

    # def testReorderTouristList(self):
    #     tourbus = self.getTourbus()
    #     tourbus.fillSeatsForTrip()
    #     tourbus.reorderTouristList()
    #     # for tourist

    def testSeatCloseToPreviousNeighbours(self):
        numTourists = 8
        tourbus = self.getTourbus(8, 8)
        bus = BusContainer(numTourists)
        seatNum = 5
        for i in range(len(tourbus.tourists)):
            tourbus.tourists[i].seatPositions.append(i)
            if i != seatNum:
                bus.add(tourbus.tourists[i], i)
        tourist = tourbus.tourists[5]
        neighbourThreshold = 3

        self.assertFalse(tourbus.seatCloseToPreviousNeighbours(tourist, 0, bus, neighbourThreshold, 1))
        self.assertTrue(tourbus.seatCloseToPreviousNeighbours(tourist, 1, bus, neighbourThreshold, 1))
        self.assertTrue(tourbus.seatCloseToPreviousNeighbours(tourist, 2, bus, neighbourThreshold, 1))
        self.assertTrue(tourbus.seatCloseToPreviousNeighbours(tourist, 3, bus, neighbourThreshold, 1))
        self.assertFalse(tourbus.seatCloseToPreviousNeighbours(tourist, 4, bus, neighbourThreshold, 1))
        self.assertTrue(tourbus.seatCloseToPreviousNeighbours(tourist, 5, bus, neighbourThreshold, 1))
        self.assertTrue(tourbus.seatCloseToPreviousNeighbours(tourist, 6, bus, neighbourThreshold, 1))
        self.assertTrue(tourbus.seatCloseToPreviousNeighbours(tourist, 7, bus, neighbourThreshold, 1))

        neighbourThreshold = 4

        self.assertFalse(tourbus.seatCloseToPreviousNeighbours(tourist, 0, bus, neighbourThreshold, 1))
        self.assertFalse(tourbus.seatCloseToPreviousNeighbours(tourist, 1, bus, neighbourThreshold, 1))
        self.assertTrue(tourbus.seatCloseToPreviousNeighbours(tourist, 2, bus, neighbourThreshold, 1))
        self.assertFalse(tourbus.seatCloseToPreviousNeighbours(tourist, 3, bus, neighbourThreshold, 1))
        self.assertFalse(tourbus.seatCloseToPreviousNeighbours(tourist, 4, bus, neighbourThreshold, 1))
        self.assertTrue(tourbus.seatCloseToPreviousNeighbours(tourist, 5, bus, neighbourThreshold, 1))
        self.assertTrue(tourbus.seatCloseToPreviousNeighbours(tourist, 6, bus, neighbourThreshold, 1))
        self.assertFalse(tourbus.seatCloseToPreviousNeighbours(tourist, 7, bus, neighbourThreshold, 1))

        neighbourThreshold = 5

        self.assertFalse(tourbus.seatCloseToPreviousNeighbours(tourist, 0, bus, neighbourThreshold, 1))
        self.assertFalse(tourbus.seatCloseToPreviousNeighbours(tourist, 1, bus, neighbourThreshold, 1))
        self.assertFalse(tourbus.seatCloseToPreviousNeighbours(tourist, 2, bus, neighbourThreshold, 1))
        self.assertFalse(tourbus.seatCloseToPreviousNeighbours(tourist, 3, bus, neighbourThreshold, 1))
        self.assertFalse(tourbus.seatCloseToPreviousNeighbours(tourist, 4, bus, neighbourThreshold, 1))
        self.assertTrue(tourbus.seatCloseToPreviousNeighbours(tourist, 5, bus, neighbourThreshold, 1))
        self.assertFalse(tourbus.seatCloseToPreviousNeighbours(tourist, 6, bus, neighbourThreshold, 1))
        self.assertFalse(tourbus.seatCloseToPreviousNeighbours(tourist, 7, bus, neighbourThreshold, 1))

        neighbourThreshold = 6

        self.assertFalse(tourbus.seatCloseToPreviousNeighbours(tourist, 0, bus, neighbourThreshold, 1))
        self.assertFalse(tourbus.seatCloseToPreviousNeighbours(tourist, 1, bus, neighbourThreshold, 1))
        self.assertFalse(tourbus.seatCloseToPreviousNeighbours(tourist, 2, bus, neighbourThreshold, 1))
        self.assertFalse(tourbus.seatCloseToPreviousNeighbours(tourist, 3, bus, neighbourThreshold, 1))
        self.assertFalse(tourbus.seatCloseToPreviousNeighbours(tourist, 4, bus, neighbourThreshold, 1))
        self.assertFalse(tourbus.seatCloseToPreviousNeighbours(tourist, 5, bus, neighbourThreshold, 1))
        self.assertFalse(tourbus.seatCloseToPreviousNeighbours(tourist, 6, bus, neighbourThreshold, 1))
        self.assertFalse(tourbus.seatCloseToPreviousNeighbours(tourist, 7, bus, neighbourThreshold, 1))

    def testGetClosenessFactor(self):
        tourbus = self.getTourbus(8, 8)

        self.assertEqual(tourbus.getCloseNessFactor(0, 1), NeightbourClassification.BESIDE.value)
        self.assertEqual(tourbus.getCloseNessFactor(0, 2), NeightbourClassification.VERTICAL.value)
        self.assertEqual(tourbus.getCloseNessFactor(0, 3), NeightbourClassification.DIAGONAL.value)
        self.assertEqual(tourbus.getCloseNessFactor(0, 4), NeightbourClassification.OTHER.value)

        self.assertEqual(tourbus.getCloseNessFactor(5, 0), NeightbourClassification.OTHER.value)
        self.assertEqual(tourbus.getCloseNessFactor(5, 1), NeightbourClassification.OTHER.value)
        self.assertEqual(tourbus.getCloseNessFactor(5, 2), NeightbourClassification.DIAGONAL.value)
        self.assertEqual(tourbus.getCloseNessFactor(5, 3), NeightbourClassification.VERTICAL.value)
        self.assertEqual(tourbus.getCloseNessFactor(5, 4), NeightbourClassification.BESIDE.value)
        self.assertEqual(tourbus.getCloseNessFactor(5, 5), NeightbourClassification.SAME.value)
        self.assertEqual(tourbus.getCloseNessFactor(5, 6), NeightbourClassification.DIAGONAL.value)
        self.assertEqual(tourbus.getCloseNessFactor(5, 7), NeightbourClassification.VERTICAL.value)

    def testGetPrevSeats(self):
        tourbus = self.getTourbus(8, 8)
        tourist1 = tourbus.tourists[0]
        tourist1.seatPositions = [0]
        tourist2 = tourbus.tourists[1]
        tourist2.seatPositions = [1]
        self.assertEqual(tourbus.getPrevSeats(tourist1, tourist2), (0, 1))

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

