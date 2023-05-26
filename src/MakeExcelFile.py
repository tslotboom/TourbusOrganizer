from openpyxl import Workbook
import argparse
from .Tourbus import Tourbus, Tourist
import string


def createWorkbook(path: str) -> Workbook:
    workbook = Workbook()
    workbook.save(path)
    return workbook


def getExcelCol(num: int):
    alphabet = string.ascii_uppercase
    numLetters = 26
    col = ""
    while num > 0:
        remainder = (num - 1) % numLetters
        num = (num - remainder) // numLetters
        col = alphabet[remainder] + col
    return col


if __name__ == "__main__":
    numTourists = 14
    numDays = 8

    tourbus = Tourbus([Tourist(str(i)) for i in range(numTourists)], numDays)
    tourbus.fillSeatsForTrip()
    tourbus.getTourists()
    tourists = tourbus.getTourists()
    tourists = sorted(tourists, key=lambda h: (h.seatPositions[0]))
    for tourist in tourists:
        print(f"{tourist} - {tourist.seatPositions}")

    workbook = createWorkbook("hello.xlsx")
    sheet = workbook.active

    for i in range(1, len(tourists) + 1):
        tourist = tourists[i]
        for j in range(len(tourist.seatPositions)):
            seat = tourist.seatPositions[j]
            key = f"{getExcelCol(i)}{j + 1}"
            sheet[key] = tourist.name
            sheet[f"{getExcelCol(i)}{j + 2}"] = seat
