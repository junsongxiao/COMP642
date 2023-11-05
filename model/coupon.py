
from datetime import datetime
class Coupon:
    def __init__(self, couponID: str, expiryDate: datetime, discount: float):
        self.__couponID = couponID
        self.__expiryDate = expiryDate
        self.__discount = discount

    # Getter methods
    def get_couponID(self):
        return self.__couponID

    def get_expiryDate(self):
        return self.__expiryDate

    def get_discount(self):
        return self.__discount

    # Setter methods
    def set_couponID(self, couponID):
        self.__couponID = couponID

    def set_expiryDate(self, expiryDate):
        self.__expiryDate = expiryDate

    def set_discount(self, discount):
        self.__discount = discount