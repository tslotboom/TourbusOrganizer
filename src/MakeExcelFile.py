from openpyxl import Workbook
import argparse
from .Tourbus import Tourbus, Tourist
import string


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
    numDays = 3

    tourbus = Tourbus([Tourist(str(i)) for i in range(numTourists)], numDays)
    tourbus.fillSeatsForTrip()
    tourbus.getTourists()
    tourists = tourbus.getTourists()
    tourists = sorted(tourists, key=lambda h: (h.seatPositions[0]))

    path = "tourbus.xlsx"
    workbook = Workbook()
    sheet = workbook.active

    sheet["A1"] = "Tourists"
    for day in range(numDays):
        sheet[f"{getExcelCol(day + 2)}1"] = f"Day {day + 1}"

    for row in range(len(tourists)):
        tourist = tourists[row]
        excelRow = row + 2
        sheet[f"A{excelRow}"] = tourist.name
        for col in range(len(tourist.seatPositions)):
            seat = tourist.seatPositions[col]
            sheet[f"{getExcelCol(col + 2)}{excelRow}"] = seat

    workbook.save(path)
