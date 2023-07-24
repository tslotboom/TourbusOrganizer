from .Tourbus import Tourbus
from .Tourist import Tourist

if __name__ == "__main__":
    numDays = 7
    numTourists = 8
    tourists = [Tourist(str(i)) for i in range(numTourists)]
    tourists[0].groupID = 1
    tourists[1].groupID = 3
    tourists[2].groupID = 2
    tourists[3].groupID = 2
    tourists[4].groupID = 3
    tourists[5].groupID = 1
    # tourists[6].groupID = 4
    # tourists[7].groupID = 5
    tourbus = Tourbus(tourists, numDays)
    tourbus.fillSeatsForTrip()

    day = 1
    for bus in tourbus.busHistory:
        print(f"Day {day}:")
        print(bus)
        day += 1

    for tourist in tourists:
        print(tourist, tourist.calculateTotalSeatScore())
