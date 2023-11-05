
class Notification:
    def __init__(self, notificationID: int, content: str):
        self.__notificationID = notificationID
        self.__createdOn = date.today()
        self.__content = content

    # Getter methods
    def get_notificationID(self):
        return self.__notificationID

    def get_createdOn(self):
        return self.__createdOn

    def get_content(self):
        return self.__content

    # Setter methods
    def set_notificationID(self, notificationID):
        self.__notificationID = notificationID

    def set_content(self, content):
        self.__content = content