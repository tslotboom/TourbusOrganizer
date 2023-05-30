from .Tourbus import Tourbus
from .Tourist import Tourist

if __name__ == "__main__":
    numDays = 7
    numTourists = 14
    tourists = [Tourist(str(i)) for i in range(numTourists)]
    tourbus = Tourbus(tourists, numDays)
    tourbus.fillSeatsForTrip()

    day = 1
    for bus in tourbus.busDays:
        print(f"Day {day}:")
        print(bus)
        day += 1
