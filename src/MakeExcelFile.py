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
    numDays = 8

    tourists = [
        Tourist("TRAVIS Linda Ms.", seatPositions=[9, 6]),
        Tourist("CLAVIER Anita Ms. & NICKENIG Stephen Mr.", seatPositions=[0, 5]),
        Tourist("DRUMHEISER Sidney Mr. & DRUMHEISER Patricia Mrs.", seatPositions=[1,2]),
        Tourist("KEROACK Marc Mr. & KEROACK Elizabeth Mrs.", seatPositions=[2,8]),
        Tourist("KERR Patricia Mrs.	& KERR John Mr.", seatPositions=[3,1]),
        Tourist("KUHNERT Sue Mrs. & KUHNERT Ralph Mr.", seatPositions=[4,7]),
        Tourist("LESTAN Anita Mrs. & LESTAN Ronald Mr.", seatPositions=[5,10]),
        Tourist("PILGRIM Sharyl Ms.	& HOLCOMB Mary Jean Ms.", seatPositions=[6,4]),
        Tourist("SCOTT Lloyd Mr. & SCOTT Cheryl Mrs.", seatPositions=[7,9]),
        Tourist("SEAVER Lucia Mrs. & SEAVER Geoffery Mr.", seatPositions=[8,3]),
        Tourist("WANCE Dennis Mr. & WANCE Patricia Mrs.", seatPositions=[10, 0])
    ]

    tourbus = Tourbus(tourists, numDays)
    tourbus.fillSeatsForTrip()
    tourbus.addOneToAllSeats()
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
