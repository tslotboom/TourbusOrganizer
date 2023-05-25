from typing import Dict

import matplotlib.pyplot as plt

from .Tourbus import Tourbus, Tourist


class Stats:

    def __init__(self, numDays: int, numTourists: int, seatScores: Dict[str, float], projectedSeatScore):
        self.numDays = numDays
        self.numTourists = numTourists
        self.seatScores = seatScores
        self.projectedSeatScore = projectedSeatScore

    def getDeviances(self):
        return [abs(self.projectedSeatScore - seatScore) for seatScore in self.seatScores.values()]

    def getAvgDeviance(self):
        deviances = self.getDeviances()
        return sum(deviances) / len(deviances)


if __name__ == "__main__":
    minDays = 1
    maxDays = 32
    maxTourists = 16
    stats = {}

    for numDays in range(minDays, maxDays):
        stats[numDays] = []
        for numTourists in range(2, maxTourists):
            tourists = [Tourist(str(i)) for i in range(numTourists)]
            tourbus = Tourbus(tourists, numDays)
            tourbus.fillSeatsForTrip()
            seatScores = {}
            for tourist in tourbus.tourists:
                seatScores[tourist.name] = tourist.calculateTotalSeatScore()
            stats[numDays].append(Stats(numDays, numTourists, seatScores, tourbus.projectedSeatScore))

    x = []
    y = []
    z = []

    plt.title("Average Deviance from Projected Seat Score vs. \n Number of Tourists vs Tour Length")
    plt.xlabel("Number of Tourists")
    plt.ylabel("Average Deviance of Tourist Seat Score \n from Projected Seat Score")

    for numDays in stats.keys():
        x.extend([i.numTourists for i in stats[numDays]])
        y.extend([i.getAvgDeviance() for i in stats[numDays]])
        z.extend(numDays for _ in range(len(stats[numDays])))

    plt.scatter(x, y, c=z, cmap='rainbow')
    plt.colorbar(label="Tour Length (Days)")
    plt.show()





