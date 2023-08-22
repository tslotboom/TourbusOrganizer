from .BusHelper import BusHelper
from typing import Optional


class Tourist(BusHelper):

    def __init__(self, name: str, groupID: Optional[int] = None, seatPositions=None):
        self.name = name
        self.groupID = groupID
        self.seatingPriority = 0
        if seatPositions is None:
            self.seatPositions = []
        else:
            self.seatPositions = seatPositions
        self.leftSeatings = 0
        self.rightSeatings = 0

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

    def inGroup(self):
        return self.groupID is not None
