from typing import List, Tuple


SPOTS_PER_ROW = 2


class BusHelper:

    def getRowAndCol(self, num: int) -> Tuple[int, int]:
        row = num // SPOTS_PER_ROW
        col = num % SPOTS_PER_ROW
        return row, col

    def calculateSeatScore(self, seatNum: int) -> int:
        return seatNum // SPOTS_PER_ROW

    def getTotalPossibleSeats(self, numTourists: int) -> int:
        return ((numTourists + 1) // 2) * 2
