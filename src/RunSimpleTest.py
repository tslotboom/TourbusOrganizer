from .Tourbus import Tourbus
from .Tourist import Tourist

if __name__ == "__main__":
    numDays = 9
    numTourists = 9
    tourists = [
        Tourist("Aguila, Laura Libier & Aguila, Daniel Alexander"),
        Tourist("Almaria, Hermenegildo Herrera"),
        Tourist("Aluri, Nirmala R & Reddy, Vasantha"),
        Tourist("Vatsamanu, Sumathi"),
        Tourist("Biermaier, Kay Marie & Cardinal, Karen Verna"),
        Tourist("Cheezum, Kevin Robert & Cheezum, Virginia Gale"),
        Tourist("Flores, Evita Almero & Flores, Jesus"),
        Tourist("Gasapo, Michael Charles & Gasapo, Sara Lynn"),
        Tourist("Hampshire, David James & Hampshire, Vivian M"),
        Tourist("Juron, Barbara Lynn & Juron, James Joseph"),
        Tourist("Liu, Jun"),
        Tourist("Musni, Evelyn Manalili & Musni, Arnel Simeon"),
        Tourist("Rizzolo, Tina H & Rizzolo, Kimtran"),
        Tourist("Scotti  Alvarado, Melissa & Mangalindan, Juaellesper Salazar"),
        Tourist("Tang, Jye & Tang, Elaine Chang"),
        Tourist("Tang, Deborah Shushin & Silpasuvan, Benjamin Tang  [10]"),
        Tourist("Silpasuvan, Catherine Chang  [8]"),
        Tourist("Villalobos, Michelle Dalmass & Villalobos, Brian Wayne"),
        Tourist("Wu, Jan Qianyu & Liu, Dahsin"),
        Tourist("Xu, Shirley S & Zheng, Xian Xian"),
        Tourist("Zhang, Xihong & Wang, Guoqing"),
        Tourist("Zheng, Jing & Zeng,  Zhonggang")
    ]

    tourbus = Tourbus(tourists, numDays)
    tourbus.fillSeatsForTrip()

    day = 1
    for bus in tourbus.busHistory:
        print(f"Day {day}:")
        print(bus)
        day += 1

    for tourist in tourists:
        print(tourist, tourist.calculateTotalSeatScore())
