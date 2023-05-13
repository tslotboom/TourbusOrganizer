import copy
from typing import List, Tuple
import numpy as np
from collections import OrderedDict

SPOTS_PER_ROW = 2


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

    def __repr__(self):
        return self.name

    def calculateTotalSeatScore(self) -> float:
        if len(self.seatPositions) == 0:
            raise RuntimeError("Can't calculate seat score, tourist hasn't sat anywhere yet")
        else:
            score = 0
            for position in self.seatPositions:
                score += self.calculateSeatScore(position)
        return score

    def alreadySatInRow(self, seatNum: int) -> bool:
        row, col = self.getRowAndCol(seatNum)
        for oldSeat in self.seatPositions:
            oldRow, oldCol = self.getRowAndCol(oldSeat)
            if col == oldCol:
                return True
        return False


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
        self.totalPossibleSpots = self.getTotalPossibleSpots(len(self.tourists))
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

    # def fillSeatsForTrip2(self):
    #     for dayNum in range(self.numDays):
    #         self.fillSeatsForDay(dayNum, self.tourists)
    #
    # def fillSeatsForDay(self, dayNum: int, tourists: List[Tourist]):
    #     bus = BusContainer(len(tourists))
    #     ignoreRowClause = False
    #     ignoreFairClause = False
    #     ignoreNeighbourClause = False
    #     ignoreOptimalClause = False
    #     ignoreBestClause = False
    #     for tourist in self.tourists:
    #         seatFound = False
    #         while not seatFound:
    #             for seatNum in range(self.totalPossibleSpots):
    #                 seat = bus.get(seatNum)
    #                 if seat is not None:
    #                     alreadySatInRow = tourist.alreadySatInRow(seatNum)
    #                     seatScoreIsFair = self.checkIfSeatScoreIsFair(tourist, seatNum)
    #                     if (not alreadySatInRow or ignoreRowClause) and \
    #                             (seatScoreIsFair or ignoreFairClause) and \
    #                             (hasNewNeighbours or ignoreNeighbourClause) and \
    #                             (seatScoreIsOptimal or ignoreOptimalClause):
    #                         bus.add(tourist, seatNum)

    def checkIfSeatScoreIsFair(self, tourist: Tourist, seatNum: int) -> bool:

        p = self.projectedSeatScore + self.SEAT_SCORE_TOLERANCE
        s = self.calculateSeatScore(seatNum)
        r = p - s
        availableSeatScores = self.getAvailableSeatScores()
        M = r - m

        return

    def getAvailableSeatScores(self, tourist: Tourist):
        allowedRepeats = self.numDays / len()
        totalPossibleSeatScores = []
        for i in range(self.totalPossibleSpots):
            if self.calculateSeatScore(i) not in totalPossibleSeatScores:
                totalPossibleSeatScores.append(self.calculateSeatScore(i))
        alreadyAttainedSeatScores = [self.calculateSeatScore(i) for i in tourist.seatPositions]
        return [i for i in totalPossibleSeatScores if i not in alreadyAttainedSeatScores]

    def getAllowedRepeats(self):
        return self.numDays // (self.totalPossibleSpots // 2)




class BusContainer(BusHelper):

    def __init__(self, numTourists):
        self.totalPossibleSpots = ((numTourists + 1) // 2) * 2
        rows = self.totalPossibleSpots // 2
        self.bus = []
        for i in range(rows):
            self.bus.append([None] * SPOTS_PER_ROW)

    def add(self, tourist: Tourist, seatNum: int):
        if seatNum < 0 or seatNum > self.totalPossibleSpots:
            raise RuntimeError(f"Seat number {seatNum} outside range of permissible seat options [{0}, "
                               f"{self.totalPossibleSpots}]")
        tourist.seatPositions.append(seatNum)
        row, col = self.getRowAndCol(seatNum)
        self.bus[row][col] = tourist

    def get(self, seatNumber: int):
        if seatNumber < 0 or seatNumber > self.totalPossibleSpots:
            raise RuntimeError(f"Seat number {seatNumber} outside range of permissible seat options [{0}, "
                               f"{self.totalPossibleSpots}]")
        row, col = self.getRowAndCol(seatNumber)
        return self.bus[row][col]

    def getRowAndCol(self, num):
        row = num // SPOTS_PER_ROW
        col = num % SPOTS_PER_ROW
        return row, col



