
from datetime import datetime,date
from typing import List, Optional

class Screening:
    def __init__(
            self,
    
            screeningDate: datetime,
            startTime: datetime,
            endTime: datetime,
            hall_id: int,
            movie_id: int, 
            hall_name: str,          
            screening_id: Optional[int] = None
        ):
        self._screening_id = screening_id
        self._screeningDate = screeningDate
        self._startTime = startTime
        self._endTime = endTime
        self._hall_id = hall_id
        self._movie_id = movie_id
        self._hall_name = hall_name
       



    # Getters
    def get_screening_id(self) -> int:
        return self._screening_id

    def get_movie_id(self) -> int:
        return self._movie_id

    def get_screeningDate(self) -> datetime:
        return self._screeningDate

    def get_startTime(self) -> datetime:
        return self._startTime

    def get_endTime(self) -> datetime:
        return self._endTime

    def get_hall_id(self) -> int:
        return self._hall_id
    

    # Setters
    def set_screening_id(self, screening_id: int):
        self._screening_id = screening_id

    def set_movie_id(self, movie_id: int):
        self._movie_id = movie_id

    def set_screeningDate(self, screeningDate: datetime):
        self._screeningDate = screeningDate

    def set_startTime(self, startTime: datetime):
        self._startTime = startTime

    def set_endTime(self, endTime: datetime):
        self._endTime = endTime

    def set_hall_id(self, hall_id: int):
        self._hall_id = hall_id

    
    def get_details(self):
        return {           

            
        "screening_id":self._screening_id ,
        "screeningDate":self._screeningDate ,
        "startTime":self._startTime ,
        "endTime":self._endTime ,
        "hall_id": self._hall_id ,
        "movie_id":self._movie_id ,
        "hall_name":self._hall_name,
        
        }
