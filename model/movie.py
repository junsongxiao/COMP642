from datetime import datetime
from typing import List, Optional

class Movie:

    def __init__(self, 
             title: str, 
             description: str, 
             durationMins: int, 
             language: str, 
             releaseDate: datetime, 
             director:str,
             country: str, 
             genre: str, 
             movie_id=None, 
             screeningList: Optional[List] = None, 
             screening_times: Optional[List[str]] = None):
    
        self._title = title
        self._description = description
        self._durationMins = durationMins
        self._language = language
        self._releaseDate = releaseDate
        self._director = director
        self._country = country
        self._genre = genre
        self._screeningList = screeningList if screeningList is not None else []
        self._movie_id = movie_id
        self._screening_times = screening_times if screening_times is not None else []

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, title: str):
        self._title = title

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, description: str):
        self._description = description

    @property
    def duration(self):
        return self._durationMins

    @duration.setter
    def duration(self, durationMins: int):
        self._durationMins = durationMins   

    @property
    def language(self) -> str:
        return self._language

    @language.setter
    def language(self, language: str):
        self._language = language

    @property
    def releaseDate(self) -> datetime:
        return self._releaseDate

    @releaseDate.setter
    def releaseDate(self, releaseDate: datetime):
        self._releaseDate = releaseDate
    
    @property
    def director(self) -> str:
        return self._director

    @director.setter
    def director(self, director: str):
        self._director = director

    @property
    def country(self) -> str:
        return self._country

    @country.setter
    def country(self, country: str):
        self._country = country

    @property
    def genre(self) -> str:
        return self._genre

    @genre.setter
    def genre(self, genre: str):
        self._genre = genre

    @property
    def movie_id(self) -> int:
        return self._movie_id

    @movie_id.setter
    def movie_id(self, movie_id: int):
        self._movie_id = movie_id

    @property
    def screeningList(self) -> List["Screening"]:
        return self._screeningList

    @screeningList.setter
    def screeningList(self, screeningList: List["Screening"]):
        self._screeningList = screeningList



    def get_details(self):
        return {
            "title": self._title,
            "releaseDate": self._releaseDate,
            "duration": self._durationMins,
            "country": self._country,
            "genre": self._genre,
            "movie_id": self._movie_id,            
            "description": self._description,            
            "language": self._language
        }
