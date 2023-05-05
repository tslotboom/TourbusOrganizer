import copy
from typing import List
import numpy as np
from collections import OrderedDict

SPOTS_PER_ROW = 2


class Tourist:

    def __init__(self, name: str):
        self.name = name
        self.seatPositions = []

    def __repr__(self):
        return self.name

    def calculateSeatScore(self) -> float:
        if len(self.seatPositions) == 0:
            raise RuntimeError("Can't calculate seat score, tourist hasn't sat anywhere yet")
        else:
            score = 0
            for position in self.seatPositions:
                score += position // SPOTS_PER_ROW
        # return score / len(self.seatPositions)
        return score


class Tourbus:

    def __init__(self, tourists: List[Tourist]):
        self.tourists = tourists
        self.busDays = []

    def fillSeatsForTrip(self):
        # even number of rows
        for i in range(2):
            self.fillSeatsForDay()
            self.reorderTouristList()
        for tourist in self.tourists:
            print(f'{tourist.name} score: {tourist.calculateSeatScore()}')

    def fillSeatsForDay(self):
        totalPossibleSpots = len(self.tourists) if len(self.tourists) % 2 == 0 else len(self.tourists) + 1
        rows = totalPossibleSpots // 2
        bus = []
        for i in range(rows):
            bus.append([None] * SPOTS_PER_ROW)
        print()
        for tourist in self.tourists:
            spotFound = False
            if len(tourist.seatPositions) == 0:
                count = 0
                while not spotFound and count < totalPossibleSpots:
                    i, j = self.getRowAndCol(count)
                    if bus[i][j] is None:
                        bus[i][j] = tourist
                        tourist.seatPositions.append(count)
                        spotFound = True
                    count += 1
            else:
                seatPositionToScoreMap = OrderedDict.fromkeys([i for i in range(totalPossibleSpots)], 0.0)
                # print(seatPositionToScoreMap)
                # Get heatmap for which seats haven't been visited yet
                for position in tourist.seatPositions:
                    refI, refJ = self.getRowAndCol(position)
                    count = 0
                    while count < totalPossibleSpots:
                        i, j = self.getRowAndCol(count)
                        score = self.getDistanceBetweenSeats(i, refI, j, refJ)
                        seatPositionToScoreMap[count] += score
                        # if count == 5 and tourist.name == "a":
                        #     print(d, position)
                        # seatPositionToScoreMap[i][j] = d
                        count += 1
                # Normalize values
                maxval = max(seatPositionToScoreMap.values())
                for key in seatPositionToScoreMap:
                    seatPositionToScoreMap[key] /= maxval

                # print(tourist.name, seatPositionToScoreMap)

                # if tourist.name == "a":
                #     string = ""
                #     for key in seatPositionToScoreMap:
                #         string += f'({key}, {round(seatPositionToScoreMap[key], 2)}) '
                #         if key % 2 == 1:
                #             string += "\n"
                #     print(string)

                # get heatmap for optimizing sitting next to different people
                personDistanceMap = OrderedDict.fromkeys(
                    [i.name for i in self.tourists if i.name != tourist.name], 0.0)

                for dayNumber in range(len(self.busDays)):
                    i, j = self.getRowAndCol(tourist.seatPositions[dayNumber])
                    for otherTourist in self.tourists:
                        if otherTourist.name != tourist.name:
                            otherI, otherJ = self.getRowAndCol(otherTourist.seatPositions[dayNumber])
                            personDistanceMap[otherTourist.name] += self.getDistanceBetweenSeats(i, otherI, j, otherJ)
                maxVal = max(personDistanceMap.values())
                #normalize values
                for key in personDistanceMap:
                    personDistanceMap[key] /= maxVal
                avgValue = sum(personDistanceMap.values()) / len(personDistanceMap)
                for key in personDistanceMap:
                    personDistanceMap[key] = personDistanceMap[key] - avgValue


                if tourist.name == "h":
                    print("personDistanceMap", personDistanceMap)
                if tourist.name == "h":
                    print(seatPositionToScoreMap)
                distances = OrderedDict.fromkeys([i for i in range(totalPossibleSpots)], 0.0)
                # distances =
                for seatnum in range(totalPossibleSpots):
                    otherI, otherJ = self.getRowAndCol(seatnum)
                    otherTourist = bus[otherI][otherJ]
                    if otherTourist is not None:
                        for key in seatPositionToScoreMap:
                            if key != seatnum:
                                i, j = self.getRowAndCol(key)
                                distance = self.getDistanceBetweenSeats(i, otherI, j, otherJ)
                                distances[key] = distance
                        avgValue = sum(distances) / len(distances)
                        for key in distances.keys():
                            distances[key] = avgValue - distances[key]
                # for key in sea
                # for i in range(len(distances)):
                #     seatPositionToScoreMap[i] += 1 / distance * personDistanceMap[otherTourist.name]

                if tourist.name == "h":
                    print(distances)

                count = 0
                seatScores = list(seatPositionToScoreMap.values())
                # print(seatDistances)
                spotIndex = None
                highestScore = 0
                while count < totalPossibleSpots:
                    i, j = self.getRowAndCol(count)
                    score = seatScores[count]
                    if score > highestScore and bus[i][j] is None:
                        highestScore = score
                        spotIndex = count
                    count += 1
                if spotIndex is None:
                    raise RuntimeError(f'Spot not found for tourist {tourist.name}')
                else:
                    i, j = self.getRowAndCol(spotIndex)
                    bus[i][j] = tourist
                    tourist.seatPositions.append(spotIndex)
        self.busDays.append(copy.deepcopy(bus))
        for i in range(len(bus)):
            print(i, bus[i][0], bus[i][0].calculateSeatScore(), bus[i][1], bus[i][1].calculateSeatScore())

    def getRowAndCol(self, num):
        row = num // SPOTS_PER_ROW
        col = num % SPOTS_PER_ROW
        return row, col

    def getDistanceBetweenSeats(self, x1, x2, y1, y2):
        return ((x1 - x2)**2 + (y1 - y2)**2)**(1/2)

    def reorderTouristList(self):
        # for tourist in self.tourists:
            # print(tourist.calculateSeatScore())
        self.tourists = sorted(self.tourists, key=lambda h: (-h.calculateSeatScore(), h.name))
        print(self.tourists)