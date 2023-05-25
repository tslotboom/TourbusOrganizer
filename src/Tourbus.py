import copy
from typing import List, Tuple, Optional
# import numpy as np
from collections import OrderedDict
from enum import Enum

SPOTS_PER_ROW = 2


class NeightbourClassification(Enum):
    SAME = 4
    BESIDE = 3
    VERTICAL = 2
    DIAGONAL = 1
    OTHER = 0


class BusHelper:

    def getRowAndCol(self, num: int) -> Tuple[int, int]:
        row = num // SPOTS_PER_ROW
        col = num % SPOTS_PER_ROW
        return row, col

    def calculateSeatScore(self, seatNum: int):
        return seatNum // SPOTS_PER_ROW


class Tourist(BusHelper):

    def __init__(self, name: str):
        self.name = name
        self.seatPositions = []

    def __repr__(self) -> str:
        return self.name

    def calculateTotalSeatScore(self) -> float:
        if len(self.seatPositions) == 0:
            return 0
        else:
            score = 0
            for position in self.seatPositions:
                score += self.calculateSeatScore(position)
        return score

    # def alreadySatInRow(self, seatNum: int) -> bool:
    #     row, col = self.getRowAndCol(seatNum)
    #     for oldSeat in self.seatPositions:
    #         oldRow, oldCol = self.getRowAndCol(oldSeat)
    #         if row == oldRow:
    #             return True
    #     return False


class BusContainer(BusHelper):

    def __init__(self, numTourists):
        self.totalPossibleSpots = ((numTourists + 1) // 2) * 2
        rows = self.totalPossibleSpots // 2
        self.bus = [[None, None] for _ in range(rows)]

    def __repr__(self) -> str:
        string = ""
        for i in range(self.totalPossibleSpots):
            row, col = self.getRowAndCol(i)
            string += f"[{self.bus[row][col]}]\t"
            if i % 2 == 1:
                string += "\n"
        return string

    def add(self, tourist: Tourist, seatNum: int):
        if seatNum < 0 or seatNum > self.totalPossibleSpots:
            raise RuntimeError(f"Seat number {seatNum} outside range of permissible seat options [{0}, "
                               f"{self.totalPossibleSpots}]")
        tourist.seatPositions.append(seatNum)
        row, col = self.getRowAndCol(seatNum)
        self.bus[row][col] = tourist

    def get(self, seatNumber: int) -> Optional[Tourist]:
        if seatNumber < 0 or seatNumber >= self.totalPossibleSpots:
            raise RuntimeError(f"Seat number {seatNumber} outside range of permissible seat options [{0}, "
                               f"{self.totalPossibleSpots}]")
        row, col = self.getRowAndCol(seatNumber)
        return self.bus[row][col]

    def getRowAndCol(self, num):
        row = num // SPOTS_PER_ROW
        col = num % SPOTS_PER_ROW
        return row, col


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

    def getTotalPossibleSeats(self, numTourists: int):
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
        # print(bus)
        self.busDays.append(bus)

    def fillBus(self, bus):
        for tourist in self.tourists:
            ignoreFairClause = False
            ignoreNeighbourClause = False
            seatFound = False
            while not seatFound:
                for seatNum in range(self.totalPossibleSeats):
                    seat = bus.get(seatNum)
                    if seat is None:
                        seatScoreIsFair = self.seatScoreIsFair(tourist, seatNum)
                        seatCloseToPreviousNeighbours = \
                            self.seatCloseToPreviousNeighbours(tourist, seatNum, bus)
                        if ((seatScoreIsFair or ignoreFairClause) and
                                (not seatCloseToPreviousNeighbours or ignoreNeighbourClause)):
                            bus.add(tourist, seatNum)
                            seatFound = True
                            break
                if not seatFound:
                    if self.neighbourThreshold < self.MAX_NEIGHBOUR_THRESHOLD:
                        self.neighbourThreshold += 1
                    elif not ignoreNeighbourClause:
                        ignoreNeighbourClause = True
                    # elif self.seatScoreTolerance > self.MAX_SEAT_SCORE_TOLERANCE:
                    #     self.seatScoreTolerance += 1
                    elif not ignoreFairClause:
                        ignoreFairClause = True
                    else:
                        raise RuntimeError("Can't find a damn seat mate")  # TODO

    def fillBusOnDayZero(self, bus):
        count = 0
        for tourist in self.tourists:
            bus.add(tourist, count)
            count += 1

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

    def getRemainingScoreAllowance(self, tourist):
        projectedWithTolerance = self.projectedSeatScore + self.seatScoreTolerance
        remainingScoreAllowance = projectedWithTolerance - tourist.calculateTotalSeatScore()
        if remainingScoreAllowance < 0:
            return 0
        return remainingScoreAllowance

    def getOptimisticSumOfRemainingScores(self, tourist):
        availableSeatScores = self.getAvailableSeatScores(tourist)
        optimisticSumOfRemainingScores = 0
        daysRemaining = self.numDays - len(tourist.seatPositions)
        for _ in range(daysRemaining):
            m = min(availableSeatScores)
            index = availableSeatScores.index(m)
            availableSeatScores.pop(index)
            optimisticSumOfRemainingScores += m
        return optimisticSumOfRemainingScores

    def getAvailableSeatScores(self, tourist: Tourist):
        allowedSeatingsPerRow = self.getAllowedSeatingsPerRow(tourist)
        totalPossibleSeatScores = []
        daysRemaining = self.numDays - len(tourist.seatPositions)
        for _ in range(daysRemaining):
            for seat in range(self.totalPossibleSeats):
                seatScore = self.calculateSeatScore(seat)
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
        lowerRange, upperRange = self.getSeatRangeForNeighbours(seatNum)
        for otherSeat in range(lowerRange, upperRange):
            otherTourist = bus.get(otherSeat)
            if otherTourist is not None and otherSeat != seatNum:
                seatCloseness = self.getCloseNessFactor(seatNum, otherSeat)
                prevSeat, otherPrevSeat = self.getPrevSeats(tourist, otherTourist, self.dayNum)
                oldSeatCloseness = self.getCloseNessFactor(prevSeat, otherPrevSeat)
                closenessFactor = seatCloseness + oldSeatCloseness
                if closenessFactor > self.neighbourThreshold:
                    return True
        return False

    def getSeatRangeForNeighbours(self, seatNum):
        lowerRange = seatNum - 3
        if lowerRange < 0:
            lowerRange = 0
        upperRange = seatNum + 3
        if upperRange > self.totalPossibleSeats:
            upperRange = self.totalPossibleSeats
        return lowerRange, upperRange

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

    def getPrevSeats(self, tourist: Tourist, otherTourist: Tourist, dayNum: int):
        try:
            prevSeat = tourist.seatPositions[dayNum - 1]
            otherPrevSeat = otherTourist.seatPositions[dayNum - 1]
        except IndexError:
            raise RuntimeError("No previous day for neighbours to be found")
        return prevSeat, otherPrevSeat

    def reorderTouristList(self):
        self.tourists = sorted(self.tourists, key=lambda h: (-h.calculateTotalSeatScore(), h.name))




