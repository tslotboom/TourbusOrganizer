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
        self.busDays = []
        self.totalPossibleSeats = self.getTotalPossibleSeats(len(self.tourists))
        self.totalRows = self.totalPossibleSeats // 2
        self.projectedSeatScore = self.getProjectedSeatScore(len(self.tourists), self.numDays)
        self.seatScoreTolerance = 1
        self.neighbourThreshold = 3
        self.dayNum = 0

    def getTotalPossibleSeats(self, numTourists: int) -> int:
        return ((numTourists + 1) // 2) * 2

    def getProjectedSeatScore(self, numTourists: int, numDays: int) -> float:
        maxSeatScorePerDay = (numTourists + 1) // 2 - 1
        avgSeatScorePerDay = maxSeatScorePerDay / 2
        return avgSeatScorePerDay * numDays

    def fillSeatsForTrip(self):
        for dayNum in range(self.numDays):
            self.dayNum = dayNum
            self.fillSeatsForDay()
            self.reorderTouristList()

    def fillSeatsForDay(self):
        bus = BusContainer(len(self.tourists))
        if self.dayNum == 0:
            self.fillBusOnDayZero(bus)
        else:
            self.fillBus(bus)
        self.busDays.append(bus)

    def fillBusOnDayZero(self, bus: BusContainer):
        count = 0
        for tourist in self.tourists:
            bus.add(tourist, count)
            count += 1

    def fillBus(self, bus: BusContainer):
        for tourist in self.tourists:
            ignoreRowClause = False
            ignoreFairClause = False
            ignoreNeighbourClause = False
            seatFound = False
            while not seatFound:
                for seatNum in range(self.totalPossibleSeats):
                    seat = bus.get(seatNum)
                    if (seat is None and
                            (not tourist.alreadySatInRow(seatNum) or ignoreRowClause) and
                            (self.seatScoreIsFair(tourist, seatNum) or ignoreFairClause) and
                            (not self.seatCloseToPreviousNeighbours(tourist, seatNum, bus) or ignoreNeighbourClause)):
                        bus.add(tourist, seatNum)
                        seatFound = True
                        break
                if not seatFound:
                    if not ignoreRowClause:
                        ignoreRowClause = True
                    elif self.neighbourThreshold < self.MAX_NEIGHBOUR_THRESHOLD:
                        self.neighbourThreshold += 1
                    elif not ignoreNeighbourClause:
                        ignoreNeighbourClause = True
                    elif not ignoreFairClause:
                        ignoreFairClause = True
                    else:
                        raise RuntimeError("Can't find a damn seat. This error shouldn't ever happen")  # TODO

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

    def reorderTouristList(self):
        newTouristList = []
        groupIDs = OrderedDict()
        noGroupIDs = []
        for tourist in self.tourists:
            if tourist.groupID is not None:
                if tourist.groupID not in groupIDs:
                    groupIDs[tourist.groupID] = []
                groupIDs[tourist.groupID].append(tourist)
            else:
                noGroupIDs.append(tourist)

        groupIDAvgSeatScores = OrderedDict().fromkeys(groupIDs.keys())

        for key in groupIDAvgSeatScores.keys():
            totalSeatScores = [i.calculateTotalSeatScore() for i in groupIDs[key]]
            s = sum(totalSeatScores)
            l = len(totalSeatScores)
            groupIDAvgSeatScores[key] = s / l
        print(groupIDAvgSeatScores.items())
        # sort groupIDAvgSeatScores in order of descending seat scores, so the group of tourists with the worst seat
        # scores are added to the list first.
        groupIDAvgSeatScores = sorted(groupIDAvgSeatScores.items(), key=lambda x: x[1], reverse=True)
        groupIDsSorted = OrderedDict()
        for keyVal in groupIDAvgSeatScores:
            groupIDsSorted[keyVal[0]] = groupIDs[keyVal[0]]
        for groupID in groupIDsSorted.keys():
            for tourist in groupIDsSorted[groupID]:
                newTouristList.append(tourist)

        noGroupIDs = sorted(noGroupIDs, key=lambda h: (-h.calculateTotalSeatScore(), h.name))
        for tourist in noGroupIDs:
            newTouristList.append(tourist)

        self.tourists = newTouristList




        # groupIDAvgSeatScores = OrderedDict(sorted(groupIDAvgSeatScores.items(), key=lambda item: item[1]))
        # print(groupIDAvgSeatScores)



        # self.tourists = sorted(self.tourists, key=lambda h: (-h.calculateTotalSeatScore(), h.name))

    def getTourists(self) -> List[Tourist]:
        return self.tourists
