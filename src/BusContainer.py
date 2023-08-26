from .BusHelper import BusHelper
from .Tourist import Tourist

from typing import Optional, Generator


class BusContainer(BusHelper):

    def __init__(self, numTourists: int):
        self.totalPossibleSpots = self.getTotalPossibleSeats(numTourists)
        rows = self.totalPossibleSpots // 2
        self.bus = [[None, None] for _ in range(rows)]
        self.oddNumOfTourists = numTourists % 2 == 1
        self.backRowSeated = False

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
        if seatNum < 0 or seatNum >= self.totalPossibleSpots:
            raise RuntimeError(f"Seat number {seatNum} outside range of permissible seat options [{0}, "
                               f"{self.totalPossibleSpots}]")
        tourist.sitDown(seatNum)
        row, col = self.getRowAndCol(seatNum)
        self.bus[row][col] = tourist
        if self.oddNumOfTourists and self.seatIsInBackRow(seatNum, self.totalPossibleSpots):
            self.backRowSeated = True


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

    def seatIsEmpty(self, seatNumber: int) -> bool:
        return self.get(seatNumber) == None

    def adjacentSeat(self, seatNumber: int) -> int:
        if seatNumber % 2 == 0:
            return seatNumber + 1
        else:
            return seatNumber - 1
