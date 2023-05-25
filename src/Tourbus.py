import copy
from typing import List, Tuple, Optional
import numpy as np
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

    def alreadySatInRow(self, seatNum: int) -> bool:
        row, col = self.getRowAndCol(seatNum)
        for oldSeat in self.seatPositions:
            oldRow, oldCol = self.getRowAndCol(oldSeat)
            if row == oldRow:
                return True
        return False


class BusContainer(BusHelper):

    def __init__(self, numTourists):
        self.totalPossibleSpots = ((numTourists + 1) // 2) * 2
        rows = self.totalPossibleSpots // 2
        self.bus = []
        for i in range(rows):
            self.bus.append([None] * SPOTS_PER_ROW)

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
        self.totalPossibleSeats = self.getTotalPossibleSpots(len(self.tourists))
        self.totalRows = self.totalPossibleSeats // 2
        self.projectedSeatScore = self.getProjectedSeatScore(len(self.tourists), self.numDays)
        self.SEAT_SCORE_TOLERANCE = 1

    def getTotalPossibleSpots(self, numTourists: int):
        return ((numTourists + 1) // 2) * 2

    def getProjectedSeatScore(self, numTourists: int, numDays: int) -> float:
        maxSeatScorePerDay = (numTourists + 1) // 2 - 1
        avgSeatScorePerDay = maxSeatScorePerDay / 2
        return avgSeatScorePerDay * numDays

    def fillSeatsForTrip(self):
        days = 9
        for i in range(days):
            self.fillSeatsForDay()
            self.reorderTouristList()
        for tourist in self.tourists:
            print(f'{tourist.name} score: {tourist.calculateTotalSeatScore()}')

    def fillSeatsForDay(self):
        totalPossibleSpots = len(self.tourists) if len(self.tourists) % 2 == 0 else len(self.tourists) + 1
        rows = totalPossibleSpots // 2
        bus = []
        touristsAlreadySeated = []
        for i in range(rows):
            bus.append([None] * SPOTS_PER_ROW)
        print()
        for tourist in self.tourists:
            if len(self.busDays) == 0:
                spotFound = False
                # if len(tourist.seatPositions) == 0:
                count = 0
                while not spotFound and count < totalPossibleSpots:
                    i, j = self.getRowAndCol(count)
                    if bus[i][j] is None:
                        bus[i][j] = tourist
                        tourist.seatPositions.append(count)
                        touristsAlreadySeated.append(tourist)
                        spotFound = True
                    count += 1
            else:
                personDistanceMap = OrderedDict.fromkeys(
                    [i.name for i in self.tourists if i.name != tourist.name], False)
                prevDayNumber = len(self.busDays) - 1
                oldSpot = tourist.seatPositions[prevDayNumber]
                row, col = self.getRowAndCol(oldSpot)
                # for i in range(totalPossibleSpots):
                #     otherRow, otherCol = self.getRowAndCol(i)
                #     otherTourist = self.busDays[prevDayNumber][otherRow][otherCol]
                #     if otherTourist.name != tourist.name:
                #         satDirectlyBeside = col == otherCol
                #         # personDistanceMap[otherTourist.name] = difference - 2  # close people neg, far people positive
                #         personDistanceMap[tourist.name] = satDirectlyBeside
                        # if difference == 1:
                        #     personDistanceMap[otherTourist.name] = 0
                        # elif difference == 2:
                        #     personDistanceMap[otherTourist.name] = 1
                        # else:
                        #     personDistanceMap[otherTourist.name] = 2
                # maxVal = max(personDistanceMap.values())
                # for key in personDistanceMap.keys():
                #     personDistanceMap[key] -= maxVal / 2

                seatScoreMap = OrderedDict.fromkeys([i for i in range(totalPossibleSpots)], 3)
                for otherTourist in touristsAlreadySeated:
                    otherSpot = otherTourist.seatPositions[prevDayNumber]
                    otherRow, otherCol = self.getRowAndCol(otherSpot)
                    satDirectlyBeside = row == otherRow
                    if satDirectlyBeside:
                        for i in range(totalPossibleSpots):
                            row, col = self.getRowAndCol(i)
                            otherRow, otherCol = self.getRowAndCol(otherTourist.seatPositions[-1])
                            difference = abs(row - otherRow) + abs(col - otherCol)
                            seatScoreMap[i] = difference
                for position in tourist.seatPositions:
                    row, col = self.getRowAndCol(position)
                    # seatScoreMap[position] -= 6 // (2 + len(self.busDays))
                    seatScoreMap[position] -= 2
                    adjacentPosition = position + 1 if position % 2 == 0 else position - 1
                    # seatScoreMap[adjacentPosition] -= 6 // (3 + len(self.busDays))
                    seatScoreMap[adjacentPosition] -= 1

                    if seatScoreMap[position] < 0:
                        seatScoreMap[position] = 0
                    if seatScoreMap[adjacentPosition] < 0:
                        seatScoreMap[adjacentPosition] = 0

                # if tourist.name == "h":
                # # print(tourist.name, personDistanceMap)
                #     print(tourist.name, seatScoreMap)

                spotFound = False
                seatScoreThreshold = 3
                while not spotFound:
                    for i in range(totalPossibleSpots):
                        row, col = self.getRowAndCol(i)
                        if bus[row][col] == None and seatScoreMap[i] >= seatScoreThreshold:
                            bus[row][col] = tourist
                            spotFound = True
                            touristsAlreadySeated.append(tourist)
                            tourist.seatPositions.append(i)
                            break
                    seatScoreThreshold -= 1
                    if seatScoreThreshold < -1:
                        raise RuntimeError("This should never happen")

            # else:
            # seatPositionToScoreMap = OrderedDict.fromkeys([i for i in range(totalPossibleSpots)], 0.0)
            # # print(seatPositionToScoreMap)
            # # Get heatmap for which seats haven't been visited yet
            # for position in tourist.seatPositions:
            #     refI, refJ = self.getRowAndCol(position)
            #     count = 0
            #     while count < totalPossibleSpots:
            #         i, j = self.getRowAndCol(count)
            #         score = self.getDistanceBetweenSeats(i, refI, j, refJ)
            #         seatPositionToScoreMap[count] += score
            #         # if count == 5 and tourist.name == "a":
            #         #     print(d, position)
            #         # seatPositionToScoreMap[i][j] = d
            #         count += 1
            # # Normalize values
            # maxval = max(seatPositionToScoreMap.values())
            # for key in seatPositionToScoreMap:
            #     seatPositionToScoreMap[key] /= maxval

            #
            # # print(tourist.name, seatPositionToScoreMap)
            #
            # # if tourist.name == "a":
            # #     string = ""
            # #     for key in seatPositionToScoreMap:
            # #         string += f'({key}, {round(seatPositionToScoreMap[key], 2)}) '
            # #         if key % 2 == 1:
            # #             string += "\n"
            # #     print(string)
            #
            # # get heatmap for optimizing sitting next to different people
            # personDistanceMap = OrderedDict.fromkeys(
            #     [i.name for i in self.tourists if i.name != tourist.name], 0.0)
            #
            # for dayNumber in range(len(self.busDays)):
            #     i, j = self.getRowAndCol(tourist.seatPositions[dayNumber])
            #     for otherTourist in self.tourists:
            #         if otherTourist.name != tourist.name:
            #             otherI, otherJ = self.getRowAndCol(otherTourist.seatPositions[dayNumber])
            #             personDistanceMap[otherTourist.name] += self.getDistanceBetweenSeats(i, otherI, j, otherJ)
            # maxVal = max(personDistanceMap.values())
            # #normalize values
            # for key in personDistanceMap:
            #     personDistanceMap[key] /= maxVal
            # avgValue = sum(personDistanceMap.values()) / len(personDistanceMap)
            # for key in personDistanceMap:
            #     personDistanceMap[key] = personDistanceMap[key] - avgValue
            #
            #
            # if tourist.name == "h":
            #     print("personDistanceMap", personDistanceMap)
            # if tourist.name == "h":
            #     print(seatPositionToScoreMap)
            # distances = OrderedDict.fromkeys([i for i in range(totalPossibleSpots)], 0.0)
            # # distances =
            # for seatnum in range(totalPossibleSpots):
            #     otherI, otherJ = self.getRowAndCol(seatnum)
            #     otherTourist = bus[otherI][otherJ]
            #     if otherTourist is not None:
            #         for key in seatPositionToScoreMap:
            #             if key != seatnum:
            #                 i, j = self.getRowAndCol(key)
            #                 distance = self.getDistanceBetweenSeats(i, otherI, j, otherJ)
            #                 distances[key] = distance
            #         avgValue = sum(distances) / len(distances)
            #         for key in distances.keys():
            #             distances[key] = avgValue - distances[key]
            # # for key in sea
            # # for i in range(len(distances)):
            # #     seatPositionToScoreMap[i] += 1 / distance * personDistanceMap[otherTourist.name]
            #
            # if tourist.name == "h":
            #     print(distances)
            #
            # seatScores = list(seatPositionToScoreMap.values())
            # print(seatDistances)

            # personDistanceMap = OrderedDict.fromkeys(
            #     [i.name for i in self.tourists if i.name != tourist.name], 0.0)
            # prevDayNumber = len(self.busDays) - 1
            # oldSpot = tourist.seatPositions[prevDayNumber]
            # row, col = self.getRowAndCol(oldSpot)
            # for i in range(totalPossibleSpots):
            #     otherRow, otherCol = self.getRowAndCol(i)
            #     otherTourist = self.busDays[prevDayNumber][otherRow][otherCol]
            #     if otherTourist.name != tourist.name:
            #         difference = abs(row - otherRow) + abs(col - otherCol)
            #         personDistanceMap[otherTourist.name] = difference
            #
            # if tourist.name == "a":
            #     print(personDistanceMap)
            #
            # count = 0
            # spotIndex = None
            # highestScore = 0
            # while count < totalPossibleSpots:
            #     i, j = self.getRowAndCol(count)
            #     score = seatPositionToScoreMap[count]
            #     if score > highestScore and bus[i][j] is None:
            #         highestScore = score
            #         spotIndex = count
            #     count += 1
            # if spotIndex is None:
            #     raise RuntimeError(f'Spot not found for tourist {tourist.name}')
            # else:
            #     i, j = self.getRowAndCol(spotIndex)
            #     bus[i][j] = tourist
            #     tourist.seatPositions.append(spotIndex)
        self.busDays.append(copy.deepcopy(bus))
        for i in range(len(bus)):
            print(i, bus[i][0], bus[i][0].calculateSeatScore(), bus[i][1], bus[i][1].calculateSeatScore())



    def getDistanceBetweenSeats(self, x1: int, x2: int, y1: int, y2: int):
        return ((x1 - x2)**2 + (y1 - y2)**2)**(1/2)

    def reorderTouristList(self):
        self.tourists = sorted(self.tourists, key=lambda h: (-h.calculateTotalSeatScore(), h.name))

    def fillSeatsForTrip2(self):
        for dayNum in range(self.numDays):
            self.fillSeatsForDay(dayNum, self.tourists)
            self.reorderTouristList()
        print(f"projected seat score: {self.projectedSeatScore}")
        for tourist in self.tourists:
            print(f"{tourist} score: {tourist.calculateTotalSeatScore()}")

    def fillSeatsForDay(self, dayNum: int, tourists: List[Tourist]):
        bus = BusContainer(len(tourists))

        # ignoreOptimalClause = False
        # ignoreBestClause = False
        if dayNum == 0:
            count = 0
            for tourist in self.tourists:
                bus.add(tourist, count)
                count += 1
        else:
            for tourist in self.tourists:
                ignoreRowClause = True
                ignoreFairClause = False
                ignoreNeighbourClause = False
                neighbourThreshold = 3
                seatFound = False
                while not seatFound:
                    for seatNum in range(self.totalPossibleSeats):
                        seat = bus.get(seatNum)
                        if seat is None:
                            alreadySatInRow = tourist.alreadySatInRow(seatNum)
                            seatScoreIsFair = self.seatScoreIsFair(tourist, seatNum)
                            seatCloseToPreviousNeighbours = self.seatCloseToPreviousNeighbours(tourist, seatNum, bus,
                                                                                               neighbourThreshold,
                                                                                               dayNum)
                            if ((not alreadySatInRow or ignoreRowClause) and
                                    (seatScoreIsFair or ignoreFairClause) and
                                    (not seatCloseToPreviousNeighbours or ignoreNeighbourClause)):
                                    # (seatScoreIsOptimal or ignoreOptimalClause ):
                                bus.add(tourist, seatNum)
                                seatFound = True
                                break
                    if not seatFound:
                        if not ignoreRowClause:
                            ignoreRowClause = True
                            # print(4)
                        elif neighbourThreshold < 5:
                            neighbourThreshold += 1
                            # print(1)
                        elif not ignoreNeighbourClause:
                            ignoreNeighbourClause = True
                            # print(2)
                        elif not ignoreFairClause:
                            ignoreFairClause = True
                            # print(3)
                        else:
                            raise RuntimeError("Can't find a damn seat mate") #TODO
        print(bus)
        self.busDays.append(bus)



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
        projectedWithTolerance = self.projectedSeatScore + self.SEAT_SCORE_TOLERANCE
        remainingScoreAllowance = projectedWithTolerance - tourist.calculateTotalSeatScore()
        return remainingScoreAllowance

    def getOptimisticSumOfRemainingScores(self, tourist):
        availableSeatScores = self.getAvailableSeatScores(tourist)
        optimisticSumOfRemainingScores = 0
        daysRemaining = self.numDays - len(tourist.seatPositions)  # TODO class variable for remaining days?
        for _ in range(daysRemaining):
            m = min(availableSeatScores)
            index = availableSeatScores.index(m)
            availableSeatScores.pop(index)
            optimisticSumOfRemainingScores += m
        return optimisticSumOfRemainingScores

    def getAvailableSeatScores(self, tourist: Tourist):
        allowedSeatingsPerRow = self.getAllowedSeatingsPerRow(tourist)
        totalPossibleSeatScores = []
        daysRemaining = self.numDays - len(tourist.seatPositions) #TODO class variable for remaining days?
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

    def seatCloseToPreviousNeighbours(self, tourist: Tourist, seatNum: int, bus: BusContainer,
                                      neighbourThreshold: int, dayNum: int) -> bool:
        lowerRange = seatNum - 3
        if lowerRange < 0:
            lowerRange = 0
        upperRange = seatNum + 3
        if upperRange > self.totalPossibleSeats:
            upperRange = self.totalPossibleSeats
        for otherSeat in range(lowerRange, upperRange):
            otherTourist = bus.get(otherSeat)
            if otherTourist is not None and otherSeat != seatNum:
                seatCloseness = self.getCloseNessFactor(seatNum, otherSeat)
                prevSeat, otherPrevSeat = self.getPrevSeats(tourist, otherTourist, dayNum)
                oldSeatCloseness = self.getCloseNessFactor(prevSeat, otherPrevSeat)
                closenessFactor = seatCloseness + oldSeatCloseness
                if closenessFactor > neighbourThreshold:
                    return True
        return False

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




