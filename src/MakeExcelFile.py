import os

from openpyxl import Workbook
from .Tourbus import Tourbus, Tourist
import string
import json


def getExcelCol(num: int):
    alphabet = string.ascii_uppercase
    numLetters = 26
    col = ""
    while num > 0:
        remainder = (num - 1) % numLetters
        num = (num - remainder) // numLetters
        col = alphabet[remainder] + col
    return col


def makeExcelFile(data: json):
    try:
        numDays = data["numDays"]
        tourists = []

        if "groupedTourists" in data:
            for group in data["groupedTourists"]:
                groupID = group["groupID"]
                tourists.extend([Tourist(i, groupID=groupID) for i in group["tourists"]])
        if "tourists" in data:
            tourists.extend([Tourist(i) for i in data["tourists"]])
    except KeyError:
        errorStr = ""
        errorStr += "Json file not set up correctly\n"
        errorStr += "Example of correct format:\n"
        with open(os.path.join(dirPath, 'sampleTourists.json')) as file:
            errorStr += json.dumps(json.load(file))
        raise KeyError(errorStr)

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
    sheet[f"{getExcelCol(numDays + 2)}1"] = f"Seat Score:"

    for row in range(len(tourists)):
        tourist = tourists[row]
        excelRow = row + 2
        sheet[f"A{excelRow}"] = tourist.name
        for col in range(len(tourist.seatPositions)):
            seat = tourist.seatPositions[col]
            sheet[f"{getExcelCol(col + 2)}{excelRow}"] = seat
        sheet[f"{getExcelCol(len(tourist.seatPositions) + 2)}{excelRow}"] = tourist.calculateTotalSeatScore()

    workbook.save(path)
    print(os.path.join(os.getcwd(), path))


if __name__ == "__main__":
    dirPath = os.path.dirname(os.path.abspath(__file__))
    try:
        with open(os.path.join(dirPath, 'tourists.json')) as file:
            data = json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found, need a file named tourists.json in {dirPath}")
    except json.JSONDecodeError:
        raise json.JSONDecodeError("Error decoding JSON file")

    makeExcelFile(data)
