from collections import OrderedDict

from .Tourist import Tourist
from .BusHelper import BusHelper
from .BusContainer import BusContainer

from typing import List, Tuple
from enum import Enum


class NeightbourClassification(Enum):
    SAME = 4
    BESIDE = 3
    VERTICAL = 2
    DIAGONAL = 1
    OTHER = 0


class Tourbus(BusHelper):

    MAX_NEIGHBOUR_THRESHOLD = 5
    MAX_SEAT_SCORE_TOLERANCE = 5

    def __init__(self, tourists: List[Tourist], numDays: int):
        if len(tourists) == 0:
            raise RuntimeError("No tourists on tour")
        if numDays <= 0:
            raise RuntimeError("Can't have a zero or negative day long tour")
        for tourist in tourists:
            if type(tourist) != Tourist:
                raise RuntimeError("Wrong data type for tourists list")
        self.tourists = tourists
        self.numDays = numDays
        self.busHistory = []
        self.totalPossibleSeats = self.getTotalPossibleSeats(len(self.tourists))
        self.totalRows = self.totalPossibleSeats // 2
        self.projectedSeatScore = self.getProjectedSeatScore(len(self.tourists), self.numDays)
        self.seatScoreTolerance = 1
        self.neighbourThreshold = 3
        self.dayNum = 0
        self.groupsSeated = []

    def getProjectedSeatScore(self, numTourists: int, numDays: int) -> float:
        maxSeatScorePerDay = (numTourists + 1) // 2 - 1
        avgSeatScorePerDay = maxSeatScorePerDay / 2
        return avgSeatScorePerDay * numDays

    def fillSeatsForTrip(self):
        for dayNum in range(self.numDays):
            self.groupsSeated = []
            self.dayNum = dayNum
            self.giveTouristsSeatingPriority()
            self.reorderTouristListForGroups()
            self.fillSeatsForDay()

    def fillSeatsForDay(self) -> None:
        bus = BusContainer(len(self.tourists))
        self.fillBus(bus)
        self.busHistory.append(bus)

    def fillBus(self, bus: BusContainer) -> None:
        for tourist in self.tourists:
            if tourist.inGroup() and self.groupSeatedOnce(tourist.groupID):
                self.seatGroupedTourist(bus, tourist)
            else:
                self.seatSingleTourist(bus, tourist)

    def groupSeatedOnce(self, groupID: int) -> bool:
        return groupID in self.groupsSeated

    def seatGroupedTourist(self, bus: BusContainer, tourist: Tourist):
        groupSeatNumbers = set()
        self.getGroupSeatNumbers(bus, groupSeatNumbers, tourist)
        seatFound = self.findSeatForGroupedTourist(bus, groupSeatNumbers, tourist)
        if not seatFound:
            self.seatSingleTourist(bus, tourist)

    def getGroupSeatNumbers(self, bus, groupSeatNumbers, tourist):
        for seatNum in range(self.totalPossibleSeats):
            if not bus.seatIsEmpty(seatNum) and bus.get(seatNum).groupID == tourist.groupID:
                groupSeatNumbers.add(seatNum)

    def findSeatForGroupedTourist(self, bus, groupSeatNumbers, tourist):
        seatFound = False
        closenessFactors = [
            NeightbourClassification.BESIDE.value,
            NeightbourClassification.VERTICAL.value,
            NeightbourClassification.DIAGONAL.value
        ]
        while not seatFound and len(closenessFactors) > 0:
            closenessFactor = closenessFactors.pop(0)
            for seatNum in range(self.totalPossibleSeats):
                adjacentSeat = bus.adjacentSeat(seatNum)
                if bus.seatIsEmpty(seatNum) and self.getCloseNessFactor(seatNum, adjacentSeat) == closenessFactor and \
                        adjacentSeat in groupSeatNumbers:
                    bus.add(tourist, seatNum)
                    seatFound = True
                    break
        return seatFound

    def seatSingleTourist(self, bus: BusContainer, tourist: Tourist):
        ignoreRowClause = False
        ignoreFairClause = False
        ignoreNeighbourClause = False
        ignoreLeftRightClause = False
        ignoreBackSeatClause = False
        seatFound = False
        while not seatFound:
            for seatNum in self.seatRangeForTourist(tourist):
                if (bus.seatIsEmpty(seatNum) and self.dayNum == 0) or \
                        (bus.seatIsEmpty(seatNum) and
                        (not tourist.alreadySatInRow(seatNum) or ignoreRowClause) and
                        (self.seatScoreIsFair(tourist, seatNum) or ignoreFairClause) and
                        (not self.seatCloseToPreviousNeighbours(tourist, seatNum, bus) or ignoreNeighbourClause) and
                        (self.seatIsOnCorrectSide(tourist, seatNum) or ignoreLeftRightClause) and
                        (not self.seatIsInBackRow(seatNum, self.totalPossibleSeats) or
                        (not bus.backRowSeated) and (not tourist.inGroup()) or ignoreBackSeatClause)):
                    bus.add(tourist, seatNum)
                    seatFound = True
                    if tourist.inGroup() and not self.groupSeatedOnce(tourist.groupID):
                        self.groupsSeated.append(tourist.groupID)
                    break
            if not seatFound:
                if not ignoreLeftRightClause:
                    ignoreLeftRightClause = True
                elif self.neighbourThreshold < self.MAX_NEIGHBOUR_THRESHOLD:
                    self.neighbourThreshold += 1
                elif not ignoreNeighbourClause:
                    ignoreNeighbourClause = True
                elif not ignoreFairClause:
                    ignoreFairClause = True
                elif not ignoreRowClause:
                    ignoreRowClause = True
                elif not ignoreBackSeatClause:
                    ignoreBackSeatClause = True
                else:
                    raise RuntimeError("Can't find a damn seat. This error shouldn't ever happen")  # TODO

    def seatRangeForTourist(self, tourist):
        if tourist.seatingPriority > self.totalPossibleSeats or tourist.seatingPriority < 0:
            raise RuntimeError(f"Invalid seating priority for tourist {tourist.name} {tourist.seatingPriority}")
        seat = tourist.seatingPriority
        yield seat
        for i in range(1, self.totalPossibleSeats):
            if seat + i < self.totalPossibleSeats:
                yield seat + i
            if seat - i >= 0:
                yield seat - i

    def seatScoreIsFair(self, tourist: Tourist, seatNum: int) -> bool:
        seatScore = self.calculateSeatScore(seatNum)
        remainingScoreAllowance = self.getRemainingScoreAllowance(tourist)

        # Temporarily add this seat to tourist's list of seats to check if the seat is fair
        tourist.seatPositions.append(seatNum)

        optimisticSumOfRemainingScores = self.getOptimisticSumOfRemainingScores(tourist)

        # remove temporarily added seat position
        tourist.seatPositions.pop()

        maxAllowableScoreToday = remainingScoreAllowance - optimisticSumOfRemainingScores
        maxAllowableScoreToday = 0 if maxAllowableScoreToday < 0 else maxAllowableScoreToday
        return seatScore <= maxAllowableScoreToday

    def getRemainingScoreAllowance(self, tourist: Tourist) -> float:
        projectedWithTolerance = self.projectedSeatScore + self.seatScoreTolerance
        remainingScoreAllowance = projectedWithTolerance - tourist.calculateTotalSeatScore()
        if remainingScoreAllowance < 0:
            return 0
        return remainingScoreAllowance

    def getOptimisticSumOfRemainingScores(self, tourist: Tourist) -> int:
        availableSeatScores = self.getAvailableSeatScores(tourist)
        optimisticSumOfRemainingScores = 0
        daysRemaining = self.numDays - len(tourist.seatPositions)
        for _ in range(daysRemaining):
            m = min(availableSeatScores)
            index = availableSeatScores.index(m)
            availableSeatScores.pop(index)
            optimisticSumOfRemainingScores += m
        return optimisticSumOfRemainingScores

    def getAvailableSeatScores(self, tourist: Tourist) -> List[int]:
        allowedSeatingsPerRow = self.getAllowedSeatingsPerRow(tourist)
        totalPossibleSeatScores = []
        daysRemaining = self.numDays - len(tourist.seatPositions)
        for _ in range(daysRemaining):
            for seatNum in range(self.totalPossibleSeats):
                seatScore = self.calculateSeatScore(seatNum)
                if allowedSeatingsPerRow[seatScore] > 0:
                    totalPossibleSeatScores.append(seatScore)
                    allowedSeatingsPerRow[seatScore] -= 1
            if max(allowedSeatingsPerRow) == 0:
                break
        return totalPossibleSeatScores

    def getAllowedSeatingsPerRow(self, tourist: Tourist) -> List[int]:
        allowedRepeats = self.getAllowedRowRepeats()
        rowsSatIn = [self.getRowAndCol(i)[0] for i in tourist.seatPositions]
        allowedSeatingsPerRow = [allowedRepeats + 1 for _ in range(self.totalRows)]
        for row in rowsSatIn:
            try:
                if allowedSeatingsPerRow[row] > 0:
                    allowedSeatingsPerRow[row] -= 1
            except IndexError:
                raise RuntimeError(f"rowsSatIn contains invalid row {row}, max rows={self.totalRows}")
        return allowedSeatingsPerRow

    def getAllowedRowRepeats(self) -> int:
        return (self.numDays - 1) // (self.totalPossibleSeats // 2)

    def seatCloseToPreviousNeighbours(self, tourist: Tourist, seatNum: int, bus: BusContainer) -> bool:
        for otherSeat in self.seatRangeForNeighbours(seatNum):
            otherTourist = bus.get(otherSeat)
            if otherTourist is not None and otherSeat != seatNum:
                seatCloseness = self.getCloseNessFactor(seatNum, otherSeat)
                prevSeat, otherPrevSeat = self.getPrevSeats(tourist, otherTourist, self.dayNum)
                oldSeatCloseness = self.getCloseNessFactor(prevSeat, otherPrevSeat)
                closenessFactor = seatCloseness + oldSeatCloseness
                if closenessFactor > self.neighbourThreshold:
                    return True
        return False

    def seatRangeForNeighbours(self, seatNum: int) -> range:
        if seatNum % 2 == 0:
            seatNum += 1
        lowerRange = seatNum - 3
        if lowerRange < 0:
            lowerRange = 0
        upperRange = seatNum + 3
        if upperRange > self.totalPossibleSeats:
            upperRange = self.totalPossibleSeats
        return range(lowerRange, upperRange)

    def getCloseNessFactor(self, seatNum: int, otherSeat: int) -> int:
        row, col = self.getRowAndCol(seatNum)
        otherRow, otherCol = self.getRowAndCol(otherSeat)
        if row == otherRow and col == otherCol:
            return NeightbourClassification.SAME.value
        elif otherRow == row:
            return NeightbourClassification.BESIDE.value
        elif otherCol == col and abs(row - otherRow) == 1:
            return NeightbourClassification.VERTICAL.value
        elif abs(row - otherRow) == 1 and abs(col - otherCol):
            return NeightbourClassification.DIAGONAL.value
        else:
            return NeightbourClassification.OTHER.value

    def getPrevSeats(self, tourist: Tourist, otherTourist: Tourist, dayNum: int) -> Tuple[int, int]:
        try:
            prevSeat = tourist.seatPositions[dayNum - 1]
            otherPrevSeat = otherTourist.seatPositions[dayNum - 1]
        except IndexError:
            raise RuntimeError("No previous day for neighbours to be found")
        return prevSeat, otherPrevSeat

    def giveTouristsSeatingPriority(self):
        touristsSorted = sorted(self.tourists, key=lambda h: (-h.calculateTotalSeatScore()))
        for i in range(len(touristsSorted)):
            touristsSorted[i].seatingPriority = i

    def reorderTouristListForGroups(self):
        newTouristList = []
        groupIDs, noGroupIDs = self.separateTouristsByGroupOrNoGroup()

        for groupID in groupIDs.keys():
            for tourist in groupIDs[groupID]:
                newTouristList.append(tourist)

        for tourist in noGroupIDs:
            newTouristList.append(tourist)

        self.tourists = newTouristList

    def separateTouristsByGroupOrNoGroup(self) -> Tuple[OrderedDict[int, List[Tourist]], List[Tourist]]:
        groupIDs = OrderedDict()
        noGroupIDs = []
        for tourist in self.tourists:
            if tourist.groupID is not None:
                if tourist.groupID not in groupIDs:
                    groupIDs[tourist.groupID] = []
                groupIDs[tourist.groupID].append(tourist)
            else:
                noGroupIDs.append(tourist)
        return groupIDs, noGroupIDs

    def getGroupIDAvgSeatScores(self, groupIDs) -> OrderedDict[int, float]:
        groupIDAvgSeatScores = OrderedDict().fromkeys(groupIDs.keys())
        for key in groupIDAvgSeatScores.keys():
            totalSeatScores = [i.calculateTotalSeatScore() for i in groupIDs[key]]
            s = sum(totalSeatScores)
            l = len(totalSeatScores)
            groupIDAvgSeatScores[key] = s / l
        return groupIDAvgSeatScores

    def seatIsOnCorrectSide(self, tourist: Tourist, seatNum: int) -> bool:
        left = seatNum % 2 == 0
        if left and tourist.leftSeatings <= tourist.rightSeatings or \
                not left and tourist.rightSeatings <= tourist.leftSeatings:
            return True

    def getTourists(self) -> List[Tourist]:
        return self.tourists

    def addOneToAllSeats(self):
        for tourist in self.tourists:
            for i in range(len(tourist.seatPositions)):
                tourist.seatPositions[i] += 1