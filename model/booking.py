
class Booking:
     
    
    def __init__(self, user_id, movie_id, date, screening_id, payment_id):
        self._booking_id = None
        self._user_id= user_id
        self._movie_id = movie_id
        self._date = date
        self._screening_id = screening_id      
        self._payment_id = payment_id
        self._notifications = []


    # Getters and Setters for booking_id
    @property
    def booking_id(self):
        return self._booking_id

    @booking_id.setter
    
    def booking_id(self, value):
        if self._booking_id is None:
            self._booking_id = value
        else:
            raise ValueError("booking_id can only be set once.")

    # Getters and Setters for username
    @property
    def user_id(self):
        return self._user_id
    
    @user_id.setter
    def user_id(self, value):
        self._user_id = value

    @property
    def movie_id(self):
        return self._movie_id
    
    @movie_id.setter
    def movie_id(self, value):
        self._movie_id = value


    
    
    # Getters and Setters for date
    @property
    def date(self):
        return self._date
    
    @date.setter
    def date(self, value):
        self._date = value

    # Getters and Setters for screening_id
    @property
    def screening_id(self):
        return self._screening_id
    
    @screening_id.setter
    def screening_id(self, value):
        self._screening_id = value



    # Getters and Setters for payment_id
    @property
    def payment_id(self):
        return self._payment_id
    
    @payment_id.setter
    def payment_id(self, value):
        self._payment_id = value

    # Getters and Setters for notifications
    @property
    def notifications(self):
        return self.__notifications

    @notifications.setter
    def notifications(self, value):
        self.__notifications = value
