from abc import ABC
# General abstract class
class General(ABC):
    def __init__(self):
        pass



class Person(General):
    def __init__(self, name, address, email, phone):
        self.__name = name
        self.__address = address
        self.__email = email
        self.__phone = phone

    # Getters
    def get_name(self):
        return self.__name

    def get_address(self):
        return self.__address
    
    def get_email(self):
        return self.__email
    
    def get_phone(self):
        return self.__phone

    # Setters
    def set_name(self, name):
        self.__name = name

    def set_address(self, address):
        self.__address = address
    
    def set_email(self, email):
        self.__email = email
    
    def set_phone(self, phone):
        self.__phone = phone

    def get_details(self):
        """
        Method to get person details.
        """
        return {
            "name": self.get_name(),
            "address": self.get_address(),
            "email": self.get_email(),
            "phone": self.get_phone()
        }  


class User(Person):

    def __init__(self, name, address, email, phone, username, password):
        super().__init__(name, address, email, phone)
        self._username = username
        self._password = password  
    # getters and setters
    def get_username(self):
        return self._username
    def get_password(self):
        return self._password
    def set_username(self, username):
        self._username = username
    def set_password(self, password):
        self._password = password


class Customer(User):
    def __init__(
        self,
        name: str,
        address: str,
        email: str,
        phone: str,
        username: str,
        password: str,
    ):
        super().__init__(name, address, email, phone, username, password)
        self.__bookingList = []
        self.__notificationList = []
    def get_booking_list(self):
        return self.__bookingList
    def get_notification_list(self):
        return self.__notificationList

class Guest(General):
    pass