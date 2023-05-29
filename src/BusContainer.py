from .BusHelper import BusHelper
from .Tourist import Tourist

from typing import Optional, Generator


class BusContainer(BusHelper):

    def __init__(self, numTourists: int):
        self.totalPossibleSpots = ((numTourists + 1) // 2) * 2
        rows = self.totalPossibleSpots // 2
        self.bus = [[None, None] for _ in range(rows)]

    def __repr__(self) -> str:
        string = ""
        i = 0
        for seat in self.yieldSeats():
            string += f"[{seat}] \t"
            if i % 2 == 1:
                string += "\n"
            i += 1
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

    def yieldSeats(self) -> Generator[Optional[Tourist], None, None]:
        for i in range(self.totalPossibleSpots):
            seat = self.get(i)
            yield seat

    # def iterateOverSeatsStartingFromIndex