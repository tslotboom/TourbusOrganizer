import unittest
from unittest.mock import Mock, call
from ..Tourbus import NeighbourClassification, Tourist, Tourbus, BusContainer
from typing import List


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

    def testFillSeatsForTrip(self):
        numDays = 8
        tourbus = self.getTourbus(8, numDays)
        tourbus.giveTouristsSeatingPriority = Mock()
        tourbus.reorderTouristList = Mock()
        tourbus.fillSeatsForDay = Mock()
        tourbus.fillSeatsForTrip()
        tourbus.giveTouristsSeatingPriority.assert_has_calls([call()] * numDays)
        tourbus.reorderTouristList.assert_has_calls([call()] * numDays)
        tourbus.fillSeatsForDay.assert_has_calls([call()] * numDays)

    def testFillSeatsForDay(self):
        tourbus = self.getTourbus(8, 8)
        self.assertEqual(len(tourbus.busHistory), 0)
        tourbus.fillSeatsForDay()
        self.assertEqual(len(tourbus.busHistory), 1)

    def testFillBus(self):
        tourbus = self.getTourbus(7, 7)
        bus = BusContainer(len(tourbus.tourists))
        tourbus.seatSingleTourist = Mock()
        tourbus.seatGroupedTourist = Mock()
        tourbus.fillBus(bus)
        calls = [call(bus, tourbus.tourists[0]),
                call(bus, tourbus.tourists[1]),
                call(bus, tourbus.tourists[2]),
                call(bus, tourbus.tourists[3]),
                call(bus, tourbus.tourists[4]),
                call(bus, tourbus.tourists[5]),
                call(bus, tourbus.tourists[6])]
        tourbus.seatSingleTourist.assert_has_calls(calls)
        tourbus.seatGroupedTourist.assert_not_called()

        tourbus = self.getTourbus(7, 7)
        bus = BusContainer(len(tourbus.tourists))

        tourbus.seatSingleTourist = Mock()
        tourbus.seatGroupedTourist = Mock()
        groupID = 1
        for tourist in tourbus.tourists:
            tourist.groupID = groupID

        def side_effect(a, b):
            tourbus.groupsSeated.append(groupID)

        tourbus.seatSingleTourist.side_effect = side_effect

        tourbus.fillBus(bus)
        calls1 = [call(bus, tourbus.tourists[0])]
        calls2 = [call(bus, tourbus.tourists[1]),
                call(bus, tourbus.tourists[2]),
                call(bus, tourbus.tourists[3]),
                call(bus, tourbus.tourists[4]),
                call(bus, tourbus.tourists[5]),
                call(bus, tourbus.tourists[6])]
        tourbus.seatSingleTourist.assert_has_calls(calls1)
        tourbus.seatGroupedTourist.assert_has_calls(calls2)

    def testGroupSeatedOnce(self):
        tourbus = self.getTourbus(7, 7)
        tourbus.groupsSeated.append(1)
        self.assertTrue(tourbus.groupSeatedOnce(1))
        self.assertFalse(tourbus.groupSeatedOnce(2))

    def testSeatGroupedTourist(self):
        tourbus = self.getTourbus(7, 7)
        bus = BusContainer(len(tourbus.tourists))
        tourbus.findSeatForGroupedTourist = Mock(return_value=True)
        tourbus.seatSingleTourist = Mock()

        tourbus.seatGroupedTourist(bus, tourbus.tourists[0])
        tourbus.findSeatForGroupedTourist.assert_called_once()
        tourbus.seatSingleTourist.assert_not_called()

        tourbus.findSeatForGroupedTourist.reset_mock()
        tourbus.seatSingleTourist.reset_mock()

        tourbus.findSeatForGroupedTourist.return_value = False
        tourbus.seatGroupedTourist(bus, tourbus.tourists[0])
        tourbus.findSeatForGroupedTourist.assert_called_once()
        tourbus.seatSingleTourist.assert_called_once()

    def testFindSeatForGroupedTourist(self):
        tourbus = self.getTourbus(8, 8)
        bus = BusContainer(len(tourbus.tourists))
        tourbus.tourists[0].groupID = 0
        self.assertFalse(tourbus.findSeatForGroupedTourist(bus, tourbus.tourists[0]))

        tourbus.tourists[1].groupID = 0
        bus.add(tourbus.tourists[1], 4)
        self.assertTrue(tourbus.findSeatForGroupedTourist(bus, tourbus.tourists[0]))
        self.assertEqual(bus.get(5), tourbus.tourists[0])

        tourbus.tourists[2].groupID = 0
        self.assertTrue(tourbus.findSeatForGroupedTourist(bus, tourbus.tourists[2]))
        self.assertEqual(bus.get(2), tourbus.tourists[2])

        bus.add(tourbus.tourists[3], 3)
        bus.add(tourbus.tourists[4], 0)
        tourbus.tourists[5].groupID = 0
        self.assertTrue(tourbus.findSeatForGroupedTourist(bus, tourbus.tourists[5]))
        self.assertEqual(bus.get(6), tourbus.tourists[5])

        tourbus.tourists[6].groupID = 0
        self.assertTrue(tourbus.findSeatForGroupedTourist(bus, tourbus.tourists[6]))
        self.assertEqual(bus.get(7), tourbus.tourists[6])

        tourbus.tourists[7].groupID = 0
        self.assertTrue(tourbus.findSeatForGroupedTourist(bus, tourbus.tourists[7]))
        self.assertEqual(bus.get(1), tourbus.tourists[7])

    def testGetGroupSeatNumbers(self):
        tourbus = self.getTourbus(7, 7)
        bus = BusContainer(len(tourbus.tourists))
        tourbus.tourists[0].groupID = 0
        tourbus.tourists[1].groupID = 0
        tourbus.tourists[2].groupID = 0
        groupSeatNumbers = tourbus.getGroupSeatNumbers(bus, tourbus.tourists[2])
        self.assertEqual(groupSeatNumbers, set())

        bus.add(tourbus.tourists[0], 0)
        bus.add(tourbus.tourists[2], 1)
        groupSeatNumbers = tourbus.getGroupSeatNumbers(bus, tourbus.tourists[2])
        self.assertEqual(groupSeatNumbers, {0, 1})

    def testSeatSingleTourist(self):
        tourbus = self.getTourbus(8, 8)
        tourist = tourbus.tourists[0]
        bus = BusContainer(len(tourbus.tourists))
        bus.seatIsEmpty = Mock(return_value=True)
        tourist.alreadySatInRow = Mock(return_value=False)
        tourbus.seatScoreIsFair = Mock(return_value=True)
        tourbus.seatCloseToPreviousNeighbours = Mock(return_value=False)
        tourbus.seatIsOnCorrectSide = Mock(return_value=True)
        tourbus.seatIsInBackRow = Mock(return_value=False)

        tourbus.dayNum = 0
        tourbus.seatSingleTourist(bus, tourist)

        bus.seatIsEmpty.assert_called_once()
        tourist.alreadySatInRow.assert_not_called()
        tourbus.seatScoreIsFair.assert_not_called()
        tourbus.seatCloseToPreviousNeighbours.assert_not_called()
        tourbus.seatIsOnCorrectSide.assert_not_called()
        tourbus.seatIsInBackRow.assert_not_called()

        tourbus.dayNum = 1
        bus.seatIsEmpty.reset_mock()
        tourbus.seatSingleTourist(bus, tourist)

        bus.seatIsEmpty.assert_has_calls([call(0), call(0)])
        tourist.alreadySatInRow.assert_called_once()
        tourbus.seatScoreIsFair.assert_called_once()
        tourbus.seatCloseToPreviousNeighbours.assert_called_once()
        tourbus.seatIsOnCorrectSide.assert_called_once()
        tourbus.seatIsInBackRow.assert_called_once()

    def testSeatRangeForTourist(self):
        tourbus = self.getTourbus(8, 8)
        tourist = tourbus.tourists[0]
        expectedRange = [0, 1, 2, 3, 4, 5, 6, 7]
        for i in tourbus.seatRangeForTourist(tourist):
            self.assertEqual(i, expectedRange.pop(0))

        tourist.seatingPriority = 4
        expectedRange = [4, 5, 3, 6, 2, 7, 1, 0]
        for i in tourbus.seatRangeForTourist(tourist):
            self.assertEqual(i, expectedRange.pop(0))

        tourist.seatingPriority = 7
        expectedRange = [7, 6, 5, 4, 3, 2, 1, 0]
        for i in tourbus.seatRangeForTourist(tourist):
            self.assertEqual(i, expectedRange.pop(0))

        with self.assertRaises(RuntimeError):
            expectedRange = [0, 1, 2, 3, 4, 5, 6, 7]
            tourist.seatingPriority = 30
            tourbus.seatRangeForTourist(tourist)
            for i in tourbus.seatRangeForTourist(tourist):
                self.assertEqual(i, expectedRange.pop(0))
        with self.assertRaises(RuntimeError):
            expectedRange = [0, 1, 2, 3, 4, 5, 6, 7]
            tourist.seatingPriority = -1
            for i in tourbus.seatRangeForTourist(tourist):
                self.assertEqual(i, expectedRange.pop(0))

    def testSeatScoreIsFair(self):
        self.helpTestSeatScoreIsFair(1, 1, [], 0, True)
        self.helpTestSeatScoreIsFair(1, 1, [], 1, True)
        self.helpTestSeatScoreIsFair(8, 1, [], 0, True)
        self.helpTestSeatScoreIsFair(8, 8, [], 0, True)
        self.helpTestSeatScoreIsFair(2, 2, [0], 0, True)

        self.helpTestSeatScoreIsFair(8, 8, [7, 7, 7, 7], 7, False)
        self.helpTestSeatScoreIsFair(8, 8, [7, 7, 7, 7], 5, False)
        self.helpTestSeatScoreIsFair(8, 8, [7, 7, 7, 7], 3, False)
        self.helpTestSeatScoreIsFair(8, 8, [7, 7, 7, 7], 1, True)

        self.helpTestSeatScoreIsFair(8, 8, [0, 1, 2, 3, 4, 5, 6], 7, True)

        self.helpTestSeatScoreIsFair(8, 8, [7, 6, 5, 4], 7, False)
        self.helpTestSeatScoreIsFair(8, 8, [7, 6, 5, 4], 6, False)
        self.helpTestSeatScoreIsFair(8, 8, [7, 6, 5, 4], 5, True)
        self.helpTestSeatScoreIsFair(8, 8, [7, 6, 5, 4], 4, True)
        self.helpTestSeatScoreIsFair(8, 8, [7, 6, 5, 4], 3, True)
        self.helpTestSeatScoreIsFair(8, 8, [7, 6, 5, 4], 2, True)
        self.helpTestSeatScoreIsFair(8, 8, [7, 6, 5, 4], 1, True)
        self.helpTestSeatScoreIsFair(8, 8, [7, 6, 5, 4], 0, True)

    def helpTestSeatScoreIsFair(self, numTourists: int, numDays: int, seatPositions: List[int], seat: int,
                                expectedIsFair: bool):
        tourbus = self.getTourbus(numTourists, numDays)
        tourist = tourbus.tourists[0]
        tourist.seatPositions = seatPositions
        tourist.totalSeatScore = tourist.calculateTotalSeatScore()
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
        tourist.totalSeatScore = tourist.calculateTotalSeatScore()
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

    def testGetAvailableSeatScores(self):
        self.helpTestGetAvailableSeatScores(1, 1, [], [0])
        self.helpTestGetAvailableSeatScores(3, 1, [], [0, 1])
        self.helpTestGetAvailableSeatScores(8, 1, [], [0, 1, 2, 3])

        self.helpTestGetAvailableSeatScores(3, 2, [2], [0])
        self.helpTestGetAvailableSeatScores(8, 1, [0], [])
        self.helpTestGetAvailableSeatScores(8, 3, [0, 7], [1, 2])
        self.helpTestGetAvailableSeatScores(8, 4, [0, 7], [1, 2])
        self.helpTestGetAvailableSeatScores(8, 5, [0, 7], [0, 1, 1, 2, 2, 3])
        self.helpTestGetAvailableSeatScores(8, 5, [0, 1, 6, 7], [1, 1, 2, 2])

        self.helpTestGetAvailableSeatScores(8, 8, [], [0, 0, 1, 1, 2, 2, 3, 3])
        self.helpTestGetAvailableSeatScores(8, 8, [0, 0, 7], [1, 1, 2, 2, 3])
        self.helpTestGetAvailableSeatScores(8, 16, [0, 0, 7], [0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3])
        self.helpTestGetAvailableSeatScores(8, 16, [0, 1, 2, 3, 4, 5, 6, 7], [0, 0, 1, 1, 2, 2, 3, 3])
        self.helpTestGetAvailableSeatScores(8, 16, [0, 1, 2, 3, 4, 5, 6, 7, 0, 1, 2], [1, 2, 2, 3, 3])
        self.helpTestGetAvailableSeatScores(8, 16, [], [0] * 4 + [1] * 4 + [2] * 4 + [3] * 4)
        self.helpTestGetAvailableSeatScores(16, 8, [], [0, 1, 2, 3, 4, 5, 6, 7])

    def helpTestGetAvailableSeatScores(self, numTourists: int, numDays: int, seatPositions: List[int],
                                       expectedAvailableSeatScores: List[int]):
        tourbus = self.getTourbus(numTourists, numDays)
        tourist = tourbus.tourists[0]
        tourist.seatPositions = seatPositions
        availableSeatScores = tourbus.getAvailableSeatScores(tourist)
        self.assertCountEqual(availableSeatScores, expectedAvailableSeatScores)

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
        tourbus.neighbourThreshold = 3

        self.assertFalse(tourbus.seatCloseToPreviousNeighbours(tourist, 0, bus))
        self.assertTrue(tourbus.seatCloseToPreviousNeighbours(tourist, 1, bus))
        self.assertTrue(tourbus.seatCloseToPreviousNeighbours(tourist, 2, bus))
        self.assertTrue(tourbus.seatCloseToPreviousNeighbours(tourist, 3, bus))
        self.assertFalse(tourbus.seatCloseToPreviousNeighbours(tourist, 4, bus))
        self.assertTrue(tourbus.seatCloseToPreviousNeighbours(tourist, 5, bus))
        self.assertTrue(tourbus.seatCloseToPreviousNeighbours(tourist, 6, bus))
        self.assertTrue(tourbus.seatCloseToPreviousNeighbours(tourist, 7, bus))

        tourbus.neighbourThreshold = 4

        self.assertFalse(tourbus.seatCloseToPreviousNeighbours(tourist, 0, bus))
        self.assertFalse(tourbus.seatCloseToPreviousNeighbours(tourist, 1, bus))
        self.assertTrue(tourbus.seatCloseToPreviousNeighbours(tourist, 2, bus))
        self.assertFalse(tourbus.seatCloseToPreviousNeighbours(tourist, 3, bus))
        self.assertFalse(tourbus.seatCloseToPreviousNeighbours(tourist, 4, bus))
        self.assertTrue(tourbus.seatCloseToPreviousNeighbours(tourist, 5, bus))
        self.assertTrue(tourbus.seatCloseToPreviousNeighbours(tourist, 6, bus))
        self.assertFalse(tourbus.seatCloseToPreviousNeighbours(tourist, 7, bus))

        tourbus.neighbourThreshold = 5

        self.assertFalse(tourbus.seatCloseToPreviousNeighbours(tourist, 0, bus))
        self.assertFalse(tourbus.seatCloseToPreviousNeighbours(tourist, 1, bus))
        self.assertFalse(tourbus.seatCloseToPreviousNeighbours(tourist, 2, bus))
        self.assertFalse(tourbus.seatCloseToPreviousNeighbours(tourist, 3, bus))
        self.assertFalse(tourbus.seatCloseToPreviousNeighbours(tourist, 4, bus))
        self.assertTrue(tourbus.seatCloseToPreviousNeighbours(tourist, 5, bus))
        self.assertFalse(tourbus.seatCloseToPreviousNeighbours(tourist, 6, bus))
        self.assertFalse(tourbus.seatCloseToPreviousNeighbours(tourist, 7, bus))

        tourbus.neighbourThreshold = 6

        self.assertFalse(tourbus.seatCloseToPreviousNeighbours(tourist, 0, bus))
        self.assertFalse(tourbus.seatCloseToPreviousNeighbours(tourist, 1, bus))
        self.assertFalse(tourbus.seatCloseToPreviousNeighbours(tourist, 2, bus))
        self.assertFalse(tourbus.seatCloseToPreviousNeighbours(tourist, 3, bus))
        self.assertFalse(tourbus.seatCloseToPreviousNeighbours(tourist, 4, bus))
        self.assertFalse(tourbus.seatCloseToPreviousNeighbours(tourist, 5, bus))
        self.assertFalse(tourbus.seatCloseToPreviousNeighbours(tourist, 6, bus))
        self.assertFalse(tourbus.seatCloseToPreviousNeighbours(tourist, 7, bus))

    def testSeatRangeForNeighbours(self):
        tourbus = self.getTourbus(8, 8)
        seatRange = tourbus.seatRangeForNeighbours(0)
        self.assertEqual(seatRange, range(0, 4))
        seatRange = tourbus.seatRangeForNeighbours(1)
        self.assertEqual(seatRange, range(0, 4))
        seatRange = tourbus.seatRangeForNeighbours(2)
        self.assertEqual(seatRange, range(0, 6))
        seatRange = tourbus.seatRangeForNeighbours(3)
        self.assertEqual(seatRange, range(0, 6))
        seatRange = tourbus.seatRangeForNeighbours(4)
        self.assertEqual(seatRange, range(2, 8))
        seatRange = tourbus.seatRangeForNeighbours(5)
        self.assertEqual(seatRange, range(2, 8))
        seatRange = tourbus.seatRangeForNeighbours(6)
        self.assertEqual(seatRange, range(4, 8))
        seatRange = tourbus.seatRangeForNeighbours(7)
        self.assertEqual(seatRange, range(4, 8))

    def testGetClosenessFactor(self):
        tourbus = self.getTourbus(8, 8)

        self.assertEqual(tourbus.getCloseNessFactor(0, 1), NeighbourClassification.BESIDE.value)
        self.assertEqual(tourbus.getCloseNessFactor(0, 2), NeighbourClassification.VERTICAL.value)
        self.assertEqual(tourbus.getCloseNessFactor(0, 3), NeighbourClassification.DIAGONAL.value)
        self.assertEqual(tourbus.getCloseNessFactor(0, 4), NeighbourClassification.OTHER.value)

        self.assertEqual(tourbus.getCloseNessFactor(5, 0), NeighbourClassification.OTHER.value)
        self.assertEqual(tourbus.getCloseNessFactor(5, 1), NeighbourClassification.OTHER.value)
        self.assertEqual(tourbus.getCloseNessFactor(5, 2), NeighbourClassification.DIAGONAL.value)
        self.assertEqual(tourbus.getCloseNessFactor(5, 3), NeighbourClassification.VERTICAL.value)
        self.assertEqual(tourbus.getCloseNessFactor(5, 4), NeighbourClassification.BESIDE.value)
        self.assertEqual(tourbus.getCloseNessFactor(5, 5), NeighbourClassification.SAME.value)
        self.assertEqual(tourbus.getCloseNessFactor(5, 6), NeighbourClassification.DIAGONAL.value)
        self.assertEqual(tourbus.getCloseNessFactor(5, 7), NeighbourClassification.VERTICAL.value)

    def testGetPrevSeats(self):
        tourbus = self.getTourbus(8, 8)
        tourist1 = tourbus.tourists[0]
        tourist1.seatPositions = [0]
        tourist2 = tourbus.tourists[1]
        tourist2.seatPositions = [1]
        self.assertEqual(tourbus.getPrevSeats(tourist1, tourist2, 1), (0, 1))

    def testGiveTouristsSeatingPriority(self):
        tourbus = self.getTourbus(8, 8)
        tourbus.giveTouristsSeatingPriority()
        for i in range(len(tourbus.tourists)):
            self.assertEqual(tourbus.tourists[i].seatingPriority, i)
        tourbus.fillSeatsForDay()
        tourbus.giveTouristsSeatingPriority()
        expected = [6, 7, 4, 5, 2, 3, 0, 1]
        for i in range(len(tourbus.tourists)):
            self.assertEqual(tourbus.tourists[i].seatingPriority, expected[i])

    def testReorderTouristList(self):
        tourbus = self.getTourbus(8, 8)
        expectedTourists = [
            tourbus.tourists[0],
            tourbus.tourists[1],
            tourbus.tourists[2],
            tourbus.tourists[3],
            tourbus.tourists[4],
            tourbus.tourists[5],
            tourbus.tourists[6],
            tourbus.tourists[7]
        ]
        tourbus.reorderTouristList()
        self.assertEqual(expectedTourists, tourbus.tourists)

        tourbus = self.getTourbus(8, 8)
        tourbus.tourists[5].groupID = 2
        tourbus.tourists[6].groupID = 2
        tourbus.tourists[7].groupID = 2
        expectedTourists = [
            tourbus.tourists[5],
            tourbus.tourists[6],
            tourbus.tourists[7],
            tourbus.tourists[0],
            tourbus.tourists[1],
            tourbus.tourists[2],
            tourbus.tourists[3],
            tourbus.tourists[4]
        ]
        tourbus.reorderTouristList()
        self.assertEqual(expectedTourists, tourbus.tourists)

        tourbus = self.getTourbus(8, 8)
        tourbus.tourists[0].groupID = 2
        tourbus.tourists[1].groupID = 2
        tourbus.tourists[2].groupID = 2
        tourbus.tourists[3].groupID = 2
        tourbus.tourists[4].groupID = 2
        tourbus.tourists[5].groupID = 2
        tourbus.tourists[6].groupID = 2
        tourbus.tourists[7].groupID = 2
        expectedTourists = [
            tourbus.tourists[0],
            tourbus.tourists[1],
            tourbus.tourists[2],
            tourbus.tourists[3],
            tourbus.tourists[4],
            tourbus.tourists[5],
            tourbus.tourists[6],
            tourbus.tourists[7]
        ]
        tourbus.reorderTouristList()
        self.assertEqual(expectedTourists, tourbus.tourists)

        tourbus = self.getTourbus(8, 8)
        tourbus.tourists[0].groupID = 2
        tourbus.tourists[7].groupID = 2
        tourbus.tourists[1].groupID = 3
        tourbus.tourists[6].groupID = 3
        tourbus.tourists[2].groupID = 1
        tourbus.tourists[5].groupID = 1
        expectedTourists = [
            tourbus.tourists[0],
            tourbus.tourists[7],
            tourbus.tourists[1],
            tourbus.tourists[6],
            tourbus.tourists[2],
            tourbus.tourists[5],
            tourbus.tourists[3],
            tourbus.tourists[4]
        ]
        tourbus.reorderTouristList()
        self.assertEqual(expectedTourists, tourbus.tourists)

    def testSeparateTouristsByGroupOrNoGroup(self):
        tourbus = self.getTourbus(8, 8)
        groupIDs, noGroupIDs = tourbus.separateTouristsByGroupOrNoGroup()
        self.assertEqual(len(groupIDs), 0)
        self.assertEqual(noGroupIDs, tourbus.tourists)

        tourbus = self.getTourbus(8, 8)
        for tourist in tourbus.tourists:
            tourist.groupID = 1
        groupIDs, noGroupIDs = tourbus.separateTouristsByGroupOrNoGroup()
        self.assertEqual(groupIDs[1], tourbus.tourists)
        self.assertEqual(len(noGroupIDs), 0)

        tourbus = self.getTourbus(8, 8)
        tourbus.tourists[0].groupID = 1
        tourbus.tourists[1].groupID = 1
        tourbus.tourists[2].groupID = 2
        tourbus.tourists[3].groupID = 2
        tourbus.tourists[4].groupID = 2
        groupIDs, noGroupIDs = tourbus.separateTouristsByGroupOrNoGroup()
        self.assertEqual(groupIDs[1], [tourbus.tourists[0], tourbus.tourists[1]])
        self.assertEqual(groupIDs[2], [tourbus.tourists[2], tourbus.tourists[3], tourbus.tourists[4]])
        self.assertEqual(noGroupIDs, [tourbus.tourists[5], tourbus.tourists[6], tourbus.tourists[7]])

    def testSeatIsOnCorrectSide(self):
        tourbus = self.getTourbus(8, 8)
        tourist = tourbus.tourists[0]
        self.assertTrue(tourbus.seatIsOnCorrectSide(tourist, 0))
        self.assertTrue(tourbus.seatIsOnCorrectSide(tourist, 1))
        tourist.leftSeatings = 1
        self.assertFalse(tourbus.seatIsOnCorrectSide(tourist, 0))
        self.assertTrue(tourbus.seatIsOnCorrectSide(tourist, 1))
        tourist.rightSeatings = 2
        self.assertTrue(tourbus.seatIsOnCorrectSide(tourist, 0))
        self.assertFalse(tourbus.seatIsOnCorrectSide(tourist, 1))

    def testGetTourists(self):
        numTourists = 5
        numDays = 5
        tourbus = self.getTourbus(numTourists, numDays)
        self.assertEqual(tourbus.getTourists(), tourbus.tourists)

    def testAddOneToAllSeats(self):
        tourbus = self.getTourbus(8, 8)
        tourbus.fillSeatsForDay()
        for i in range(len(tourbus.tourists)):
            self.assertEqual(tourbus.tourists[i].seatPositions[0], i)
        tourbus.addOneToAllSeatPositions()
        for i in range(len(tourbus.tourists)):
            self.assertEqual(tourbus.tourists[i].seatPositions[0], i + 1)





