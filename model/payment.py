from datetime import datetime
class Payment:
    def __init__(self, amount: float, createdOn: datetime, paymentID: str):
        self.__amount = amount
        self.__createdOn = createdOn
        self.__paymentID = paymentID
        self.__coupon = None  # New attribute to hold the Coupon object

    # Getter methods
    def get_amount(self):
        return self.__amount

    def get_createdOn(self):
        return self.__createdOn

    def get_paymentID(self):
        return self.__paymentID

    def get_coupon(self) -> "Coupon":
        return self.__coupon

    # Setter methods
    def set_amount(self, amount):
        self.__amount = amount

    def set_createdOn(self, createdOn):
        self.__createdOn = createdOn

    def set_paymentID(self, paymentID):
        self.__paymentID = paymentID

    def set_coupon(self, coupon: "Coupon"):
        if coupon.get_expiryDate() > datetime.now():
            self.__coupon = coupon
        else:
            print("Coupon has expired!")
