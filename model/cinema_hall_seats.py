
class CinemaHallSeat:
    def __init__(
        self,
        seat_id: int,
        hall_id: int,
        seatNumber: int,
        seatColumn: int,
        seatType: int,
        isReserved: bool,
        seatPrice: float,
    ):
        self.__seat_id = seat_id
        self.__hall_id = hall_id
        self.__seatNumber = seatNumber
        self.__seatColumn = seatColumn
        self.__seatType = seatType
        self.__isReserved = isReserved
        self.__seatPrice = seatPrice

    # Getters
    def get_seat_id(self):
        return self.__seat_id

    def get_hall_id(self):
        return self.__hall_id

    def get_seatNumber(self):
        return self.__seatNumber

    def get_seatColumn(self):
        return self.__seatColumn

    def get_seatType(self):
        return self.__seatType

    def get_isReserved(self):
        return self.__isReserved

    def get_seatPrice(self):
        return self.__seatPrice

    # Setters
    def set_seatNumber(self, seatNumber):
        self.__seatNumber = seatNumber

    def set_seatColumn(self, seatColumn):
        self.__seatColumn = seatColumn

    def set_seatType(self, seatType):
        self.__seatType = seatType

    def set_isReserved(self, isReserved):
        self.__isReserved = isReserved

    def set_seatPrice(self, seatPrice):
        self.__seatPrice = seatPrice
