
class CinemaHall:
    def __init__(self, hall_id: int, name: str, totalSeats: int):
        self.__hall_id = hall_id
        self.__name = name
        self.__totalSeats = totalSeats
        self.__listOfSeats = []

    # Getters
    def get_hall_id(self):
        return self.__hall_id

    def get_name(self):
        return self.__name

    def get_totalSeats(self):
        return self.__totalSeats

    def get_listOfSeats(self):
        return self.__listOfSeats

    # Setters
    def set_name(self, name):
        self.__name = name

    def set_totalSeats(self, totalSeats):
        self.__totalSeats = totalSeats

    def set_listOfSeats(self, listOfSeats):
        self.__listOfSeats = listOfSeats