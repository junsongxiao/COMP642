from abc import ABC
from datetime import datetime, date
from typing import List, Optional



class FileUtility:
    """Commonly shared methods for each class."""
    
    @staticmethod
    def read_from_file(filename: str) -> list:
        try:
            with open(filename, 'r') as file:
                return file.readlines()
        except Exception as e:
            print(f"Error reading from {filename}: {e}")
            return []

    @staticmethod
    def write_to_file(filename: str, data: list) -> bool:
        try:
            with open(filename, 'w') as file:
                file.writelines(data)
            return True
        except Exception as e:
            print(f"Error writing to {filename}: {e}")
            return False

    @staticmethod
    def append_to_file(filename: str, data: str) -> bool:
        """Append data to a file."""
        try:
            with open(filename, 'a') as file:
                file.write(data + "\n")  # Adding a newline for consistency
            return True
        except Exception as e:
            print(f"Error appending to {filename}: {e}")
            return False


    
# class Person(General):
#     def __init__(self, name, address, email, phone):
#         self.__name = name
#         self.__address = address
#         self.__email = email
#         self.__phone = phone

#     # Getters
#     def get_name(self):
#         return self.__name

#     def get_address(self):
#         return self.__address
    
#     def get_email(self):
#         return self.__email
    
#     def get_phone(self):
#         return self.__phone

#     # Setters
#     def set_name(self, name):
#         self.__name = name

#     def set_address(self, address):
#         self.__address = address
    
#     def set_email(self, email):
#         self.__email = email
    
#     def set_phone(self, phone):
#         self.__phone = phone

#     def get_details(self):
#         """
#         Method to get person details.
#         """
#         return {
#             "name": self.get_name(),
#             "address": self.get_address(),
#             "email": self.get_email(),
#             "phone": self.get_phone()
#         }  

class Guest(General):

    def register(self, name: str, address: str, email: str, phone: str, username: str, password: str) -> bool:
        """ 
        Handles guest registration by creating a new Customer instance 
        and registering them as a user.
        """
        
        # Create a new Customer instance with the provided details
        new_customer = Customer(name=name, address=address, email=email, phone=phone)
        
        # Register the customer using the User class's register method
        return new_customer.register(username=username, password=password, email=email)



class User(Person):
    logged_in_users = []

    def __init__(self, name, address, email, phone, username, password):
        super().__init__(name, address, email, phone)
        self._username = username
        self._password = password  

    def get_username(self):
        return self._username

    @classmethod
    def get_all_users(cls):
        users = []
        lines = FileUtility.read_from_file("user.txt")
        for line in lines:
            user_data = line.strip().split(",")
            users.append(user_data[0])
        return users
    
    @classmethod
    def get_current_user_username(cls):
        return cls.logged_in_users[-1] if cls.logged_in_users else None
    
    @classmethod
    def get_current_user_type(cls):
        current_username = cls.get_current_user_username()
        if not current_username:
            return None

        # Retrieve user type from user.txt (or another mechanism)
        # This is a placeholder and will depend on how you store the user type
        lines = FileUtility.read_from_file("user.txt")
        for line in lines:
            user_data = line.strip().split(",")
            if user_data[0] == current_username:
                return user_data[6]  # Assuming the user type is stored in the 7th column of user.txt

        return None


    
    @classmethod
    def login(cls, username, password):
        """
        Method to login the user.
        Validates the provided credentials against stored user data in a file.
        """
        lines = FileUtility.read_from_file("user.txt")
        for line in lines:
            user_data = line.strip().split(",")
            if user_data[0] == username and user_data[5] == password:  
                cls.logged_in_users.append(username)
                return User(user_data[0], user_data[1], user_data[2], user_data[3], user_data[4], user_data[5])
        return False


    @classmethod
    def logout(cls, username):
        """
        Method to logout the user.
        Removes the user from the list of logged-in users.
        """
        if username in cls.logged_in_users:
            cls.logged_in_users.remove(username)
            return True
        return False

    def register(self, username, password, email):
        """
        Method to register a new user.
        """
        # For simplicity, we directly set the attributes here
        # Ideally, we would validate and possibly hash the password
        self._username = username
        self._password = password
        self._email = email

        # Save user data to a file
        user_data = [self.name, self.address, self.email, self.phone, self._username, self._password]
        FileUtility.append_to_file("user.txt", ",".join(user_data))

    def reset_password(self, new_password):
        """
        Method to reset the user's password.
        """
        self._password = new_password
        # Update the password in the file
        lines = FileUtility.read_from_file("user.txt")
        for index, line in enumerate(lines):
            user_data = line.strip().split(",")
            if user_data[0] == self._username:
                user_data[5] = new_password
                lines[index] = ",".join(user_data) + "\n"
                break
        FileUtility.write_to_file("user.txt", lines)


# Complete the deleteScreening method and finalize the Admin class

class Admin(User):
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
        self.__movies = []
        self.__screenings = []



    # Getters
    def get_movies(self) -> list:
        return self.__movies

    def get_screenings(self) -> list:
        return self.__screenings

    # Setters
    def set_movies(self, movies: list):
        self.__movies = movies

    def set_screenings(self, screenings: list):
        self.__screenings = screenings

    def cancel_movie(self, title: str) -> bool:
        return Movie.delete_movie(title)

    def cancel_screening(self, screening_id: str) -> bool:
        return Screening.remove_screening(screening_id)

    def get_next_movie_id(self) -> int:
        movies =FileUtility.read_from_file('movies.txt')
        if not movies:
            return 1
        last_line = movies[-1]
        last_id = int(last_line.split(',')[0])
        return last_id + 1

    def get_next_screening_id(self) -> int:
        screenings = FileUtility.read_from_file('screenings.txt')
        if not screenings:
            return 1
        last_line = screenings[-1]
        last_id = int(last_line.split(',')[0])
        return last_id + 1

    def addMovie(self, title, description, durationMins, language, releaseDate, country, genre) -> bool:
        movie_id = self.get_next_movie_id()
        movie_entry = f"{movie_id},{title},{description},{durationMins},{language},{releaseDate},{country},{genre}\n"
        success = FileUtility.read_from_file('movies.txt', [movie_entry])
        return success

    def updateMovie(self, movie_id, new_title=None, new_description=None, new_durationMins=None, new_language=None, new_releaseDate=None, new_country=None, new_genre=None) -> bool:
        movies = FileUtility.read_from_file('movies.txt')
        for index, movie in enumerate(movies):
            movie_details = movie.strip().split(',')
            if movie_details[0] == str(movie_id):
                if new_title:
                    movie_details[1] = new_title
                if new_description:
                    movie_details[2] = new_description
                if new_durationMins:
                    movie_details[3] = new_durationMins
                if new_language:
                    movie_details[4] = new_language
                if new_releaseDate:
                    movie_details[5] = new_releaseDate
                if new_country:
                    movie_details[6] = new_country
                if new_genre:
                    movie_details[7] = new_genre
                movies[index] = ','.join(movie_details) + '\n'
                break
        success = FileUtility.read_from_file('movies.txt', movies)
        return success

    def deleteMovie(self, movie_title) -> bool:
        movies = FileUtility.read_from_file('movies.txt')
        movies = [movie for movie in movies if not movie.startswith(movie_title + ',')]
        success = FileUtility.read_from_file('movies.txt', movies)
        return success

    def addScreening(self, movie_title, screeningDate, startTime, endTime, hall) -> bool:
        screening_id = self.get_next_screening_id()
        screening_entry = f"{screening_id},{screeningDate},{startTime},{endTime},{hall}\n"
        success = self._write_to_file('screenings.txt', [screening_entry])
        return success

    def updateScreening(self, screening_id, new_screeningDate=None, new_startTime=None, new_endTime=None, new_hall=None) -> bool:
        screenings = FileUtility.read_from_file('screenings.txt')
        for index, screening in enumerate(screenings):
            screening_details = screening.strip().split(',')
            if screening_details[0] == str(screening_id):
                if new_screeningDate:
                    screening_details[1] = new_screeningDate
                if new_startTime:
                    screening_details[2] = new_startTime
                if new_endTime:
                    screening_details[3] = new_endTime
                if new_hall:
                    screening_details[4] = new_hall
                screenings[index] = ','.join(screening_details) + '\n'
                break
        success = self._write_to_file('screenings.txt', screenings)
        return success

    def deleteScreening(self, screening_id) -> bool:
        screenings = FileUtility.read_from_file('screenings.txt')
        screenings = [screening for screening in screenings if not screening.startswith(str(screening_id) + ',')]
        success = self._write_to_file('screenings.txt', screenings)
        return success

# FrontDeskStaff class inheriting from User
class FrontDeskStaff(User):
    def makeBooking(self, movie_title, screening_time, seats, customer_username, payment_method, coupon=None):
        # Retrieve the movie and screening details
        movie = Movie.search_movies(title=movie_title)[0]
        screening = [s for s in movie.get_screenings() if s.get_schedule() == screening_time][0]
        
        # Use the customer's username to retrieve the customer object
        customer = next((user for user in User.get_all_users() if user.get_username() == customer_username), None)
        if not isinstance(customer, Customer):
            raise ValueError("Invalid customer username provided.")
        
        # Proceed to make the booking on behalf of the customer
        success = customer.makeBooking(screening, seats, coupon)
        if not success:
            raise Exception("Failed to make booking.")
        
        # Process payment (for simplicity, we'll just print a message)
        print(f"Payment of {screening.get_price()} received via {payment_method}.")
        return True

    # def cancelBooking(self, booking_id):
    #     # Retrieve the booking details
    #     booking = next((b for b in Booking.get_all_bookings() if b.get_booking_id() == booking_id), None)
    #     if not booking:
    #         raise ValueError("Invalid booking ID provided.")
        
    #     # Cancel the booking
    #     success = booking.cancel()
    #     if not success:
    #         raise Exception("Failed to cancel booking.")
        
    #     # Process refund (for simplicity, we'll just print a message)
    #     print(f"Refund of {booking.get_price()} processed.")
    #     return True-> bool:
    #     return True
    def cancelBooking(self, booking_id):
        # Retrieve the booking based on booking ID
        booking = self.get_booking_by_id(booking_id)
        if not booking:
            return False
        
        # Cancel the booking
        self.bookings.remove(booking)
        
        # Send a notification to the customer
        notification_content = f"Your booking with ID {booking_id} has been canceled."
        booking.customer.send_notification(notification_content)
        
        return True

    def login(self) -> bool:
        return True

    def logout(self) -> bool:
        return True

    def resetPassword(self) -> bool:
        return True
    
    def cancel_booking(self, booking_id: str) -> bool:
        return Booking.remove_booking(booking_id)




# class Movie:
#     FILE_PATH = "movies.txt"
#     DATE_FORMAT = "%Y-%m-%d"

#     def __init__(self, title: str, description: str, durationMins: int, language: str, releaseDate: datetime, country: str, genre: str, movie_id=None, screeningList: Optional[List["Screening"]] = None, screening_times: Optional[List[str]] = None):
#         self.__title = title
#         self.__description = description
#         self.__durationMins = durationMins
#         self.__language = language
#         self.__releaseDate = releaseDate
#         self.__country = country
#         self.__genre = genre
#         if screeningList is None:
#             screeningList = []
#         self.__screeningList = screeningList
#         self.__movie_id = movie_id
#         if screening_times is None:
#             screening_times = []
#         self.__screening_times = screening_times

#     # Getters
#     def get_title(self) -> str:
#         return self.__title

#     def get_description(self) -> str:
#         return self.__description

#     def get_durationMins(self) -> int:
#         return self.__durationMins

#     def get_language(self) -> str:
#         return self.__language

#     def get_releaseDate(self) -> datetime:
#         return self.__releaseDate

#     def get_country(self) -> str:
#         return self.__country

#     def get_genre(self) -> str:
#         return self.__genre

#     def get_movie_id(self) -> int:
#         return self.__movie_id

#     def get_screenings(self) -> List["Screening"]:
#         return [screening for screening in Screening.get_all_screenings() if screening.get_movie_id() == self.__movie_id]

#     def add_screening(self, screening: "Screening"):
#         # Check if screening is already associated with another movie
#         for movie in Movie.get_all_movies():
#             if screening in movie.__screeningList:
#                 raise ValueError(f"Screening on {screening.get_screeningDate()} at {screening.get_startTime()} is already associated with the movie {movie.get_title()}")
#         self.__screeningList.append(screening)

#     def print_screenings(self):
#         """Print the screenings associated with the movie."""
#         for screening in self.__screeningList:
#             print(screening.get_schedule())

#     def get_screening_times(self) -> List[str]:
#         return self.__screening_times
    

#     # Setters
#     def set_title(self, title: str):
#         self.__title = title

#     def set_description(self, description: str):
#         self.__description = description

#     def set_durationMins(self, durationMins: int):
#         self.__durationMins = durationMins

#     def set_language(self, language: str):
#         self.__language = language

#     def set_releaseDate(self, releaseDate: datetime):
#         self.__releaseDate = releaseDate

#     def set_country(self, country: str):
#         self.__country = country

#     def set_genre(self, genre: str):
#         self.__genre = genre

#     def set_movie_id(self, movie_id: int):
#         self.__movie_id = movie_id

#     def set_screenings(self, screenings: List["Screening"]):
#         self.__screeningList = screenings
    
#     def get_details(self):
#         return {
#             "title": self.__title,
#             "release_date": self.__releaseDate,
#             "duration": self.__durationMins,
#             "rating": self.__country,
#             "genre": self.__genre,
#             "director": self.__movie_id,
            
#             "description": self.__description,
            
#             "language": self.__language
#         }


    # @classmethod
    # def load_all_movies(cls) -> List["Movie"]:
    #     """Load all movies from the movies.txt file."""
    #     movies = []
    #     movie_entries = FileUtility.read_from_file('movies.txt')
    #     for entry in movie_entries:
    #         movie_id, title, description, duration_mins, language, release_date, country, genre = entry.strip().split(',')
    #         movie = Movie(title, description, duration_mins, language, datetime.strptime(release_date, cls.DATE_FORMAT), country, genre, movie_id)
    #         movies.append(movie)
    #     return movies
    
    # @classmethod
    # def search_movies(cls, title=None, language=None, genre=None, release_date=None) -> List["Movie"]:
    #     """Search for movies based on certain criteria."""
    #     all_movies = cls.load_all_movies()
        
    #     # Filter movies based on provided criteria
    #     filtered_movies = all_movies
    #     if title:
    #         filtered_movies = [movie for movie in filtered_movies if title.lower() in movie.get_title().lower()]
    #     if language:
    #         filtered_movies = [movie for movie in filtered_movies if language.lower() == movie.get_language().lower()]
    #     if genre:
    #         filtered_movies = [movie for movie in filtered_movies if genre.lower() == movie.get_genre().lower()]
    #     if release_date:
    #         filtered_movies = [movie for movie in filtered_movies if release_date == movie.get_releaseDate()]
        
    #     return filtered_movies

    # @classmethod
    # def add_movie(cls, movie_obj: "Movie") -> bool:
    #     """Adds a movie to the movies.txt file."""
    #     movie_data = [
    #         movie_obj.get_title(),
    #         movie_obj.get_description(),
    #         str(movie_obj.get_durationMins()),
    #         movie_obj.get_language(),
    #         movie_obj.get_releaseDate().strftime(cls.DATE_FORMAT),
    #         movie_obj.get_country(),
    #         movie_obj.get_genre()
    #     ]
    #     return FileUtility.read_from_file('movies.txt')

    # @classmethod
    # def search_movies(cls, title=None, language=None, genre=None, release_date=None) -> List["Movie"]:
    #     all_movies = cls.get_all_movies()

    #     # Filter movies based on the provided criteria
    #     if title:
    #         all_movies = [movie for movie in all_movies if title.lower() in movie.get_title().lower()]
        
    #     if language:
    #         all_movies = [movie for movie in all_movies if language.lower() == movie.get_language().lower()]
        
    #     if genre:
    #         all_movies = [movie for movie in all_movies if genre.lower() == movie.get_genre().lower()]
        
    #     if release_date:
    #         all_movies = [movie for movie in all_movies if release_date == movie.get_releaseDate()]

    #     return all_movies

    # @classmethod
    # def get_movie_by_id(cls, movie_id: int) -> Optional["Movie"]:
    #     all_movies = cls.get_all_movies()
    #     for movie in all_movies:
    #         if movie.get_movie_id() == movie_id:
    #             return movie
    #     return None
    
    # @classmethod
    # def view_details_by_id(cls, movie_id):
    #     """Retrieve movie details based on its ID."""
    #     all_movies = cls.load_all_movies()
    #     target_movie = next((movie for movie in all_movies if movie.get_id() == movie_id), None)
        
    #     if target_movie:
    #         return str(target_movie)
        
    #     return "Movie not found."

    # @classmethod
    # def add_screening_to_movie(cls, screening: "Screening"):
    #     # Check if screening is already associated with another movie
    #     for movie in Movie.get_all_movies():
    #         if screening in movie.__screeningList:
    #             raise ValueError(f"Screening on {screening.get_screeningDate()} at {screening.get_startTime()} is already associated with the movie {movie.get_title()}")
    #     self.__screeningList.append(screening)

    # @classmethod
    # def get_all_movies(cls) -> List["Movie"]:
    #     return cls.load_all_movies()

    # @classmethod
    # def update_movie(cls, title: str, updated_movie_obj: "Movie") -> bool:
    #     """Updates movie details in the movies.txt file based on the title."""
    #     movies = cls.get_all_movies()
    #     updated = False
    #     for index, movie in enumerate(movies):
    #         if movie.get_title() == title:
    #             movies[index] = updated_movie_obj
    #             updated = True
    #             break
    #     if updated:
    #         movie_data_list = []
    #         for movie in movies:
    #             movie_data = [
    #                 movie.get_title(),
    #                 movie.get_description(),
    #                 str(movie.get_durationMins()),
    #                 movie.get_language(),
    #                 movie.get_releaseDate().strftime(cls.DATE_FORMAT),
    #                 movie.get_country(),
    #                 movie.get_genre()
    #             ]
    #             movie_data_list.append(",".join(movie_data) + "\n")
    #         FileUtility.write_to_file('movie.txt', movie_data_list)
    #         return True
    #     return False

    # @classmethod
    # def delete_movie(cls, title: str) -> bool:
    #     """Deletes a movie from the movies.txt file based on the title."""
    #     movies = cls.get_all_movies()
    #     remaining_movies = [movie for movie in movies if movie.get_title() != title]
    #     if len(remaining_movies) != len(movies):
    #         movie_data_list = []
    #         for movie in remaining_movies:
    #             movie_data = [
    #                 movie.get_title(),
    #                 movie.get_description(),
    #                 str(movie.get_durationMins()),
    #                 movie.get_language(),
    #                 movie.get_releaseDate().strftime("%Y-%m-%d"),
    #                 movie.get_country(),
    #                 movie.get_genre()
    #             ]
    #             movie_data_list.append(','.join(movie_data))
            
    #         FieldUtility.write_to_file("movies.txt", '\n'.join(movie_data_list))
    #         return True
    #     return False

from datetime import datetime
from typing import List, Optional

# class Screening:
#     def __init__(
#         self,
#         screeningDate: datetime,
#         startTime: datetime,
#         endTime: datetime,
#         hall: "CinemaHall",
#         movie: Optional["Movie"] = None,
#         movie_id: Optional[int] = None
#     ):
#         self.__screeningDate = screeningDate
#         self.__startTime = startTime
#         self.__endTime = endTime
#         self.__hall = hall
#         self.__movie = movie
#         self.__movie_id = movie_id

#     # Getters
#     def get_movie(self) -> "Movie":
#         return self.__movie

#     def get_movie_id(self) -> int:
#         return self.__movie_id

#     def get_screeningDate(self) -> datetime:
#         return self.__screeningDate

#     def get_startTime(self) -> datetime:
#         return self.__startTime

#     def get_endTime(self) -> datetime:
#         return self.__endTime

#     def get_hall(self) -> "CinemaHall":
#         return self.__hall

#     # Setters
#     def set_movie(self, movie: "Movie"):
#         self.__movie = movie

#     def set_movie_id(self, movie_id: int):
#         self.__movie_id = movie_id

#     def set_screeningDate(self, screeningDate: datetime):
#         self.__screeningDate = screeningDate

#     def set_startTime(self, startTime: datetime):
#         self.__startTime = startTime

#     def set_endTime(self, endTime: datetime):
#         self.__endTime = endTime

#     def set_hall(self, hall: "CinemaHall"):
#         self.__hall = hall

#     def are_seats_available(self, seats):
#         # For this example, I'll assume that a screening has a seating matrix and 
#         # the method checks if the provided seats are available.
#         # The actual implementation would depend on how you store and check seat availability.
#         for row, col in seats:
#             if self.seating_matrix[row][col] == 1:  # Assuming 1 indicates a booked seat
#                 return False
#         return True
    
#     def get_price_for_seats(self, seats: List[str]) -> float:
#         """Compute the total price for a set of seats for this screening."""
#         # Assuming seats is a list of seat IDs
#         all_seats = CinemaHallSeat.get_all_seats_for_hall(self._hall_id)
        
#         total_price = 0
#         for seat in all_seats:
#             seat_id, _, _, _, _, price = seat.split(',')
#             if seat_id in seats:
#                 total_price += float(price)
        
#         return total_price
    
    # @classmethod
    # def get_screening_by_movie_and_datetime(cls, movie_title, screening_datetime_str):
    #     # Convert string to datetime object
    #     screening_datetime = datetime.datetime.strptime(screening_datetime_str, '%Y-%m-%d %H:%M')
        
    #     # Find the screening matching the movie title and datetime
    #     for screening in cls.get_all_screenings():
    #         if screening.get_movie() == movie_title and screening.get_startTime() == screening_datetime:
    #             return screening
    #     return None
    
    # @classmethod
    # def get_hall_id_by_screening_datetime(cls, movie_title, screening_datetime):
    #     # Fetch the screening based on movie title and datetime
    #     screening = Screening.get_screening_by_movie_and_datetime(movie_title, screening_datetime)
    #     if not screening:
    #         return None
    #     return screening.get_hall()
    
    # @classmethod
    # def get_all_screenings(cls) -> List["Screening"]:
    #     raw_data = FileUtility.read_from_file("screenings.txt")
    #     screenings = []
        
    #     for entry in raw_data:
    #         attributes = entry.split(',')
    #         if len(attributes) != 5:
    #             print(f"Skipping invalid line in screenings.txt: {entry}")
    #             continue
            
    #         screening_id, movie_id, screening_date, start_time, end_time = attributes
    #         screening = Screening(
    #             datetime.strptime(screening_date, "%Y-%m-%d"),
    #             datetime.strptime(start_time, "%H:%M"),
    #             datetime.strptime(end_time, "%H:%M"),
    #             None,  # Placeholder for CinemaHall
    #             movie_id=int(movie_id)
    #         )
    #         screenings.append(screening)
        
    #     return screenings

    # @classmethod
    # def add_screening(cls, screening: "Screening"):
    #     screening_data = [
    #         str(screening.get_movie_id()),
    #         screening.get_screeningDate().strftime("%Y-%m-%d"),
    #         screening.get_startTime().strftime("%H:%M"),
    #         screening.get_endTime().strftime("%H:%M"),
    #         str(screening.get_hall())  # Assuming get_hall() returns a string representation
    #     ]
    #     FileUtility.write_to_file("screenings.txt", ",".join(screening_data))

    # @classmethod
    # def remove_screening(cls, screening_id: int) -> bool:
    #     screenings = cls.get_all_screenings()
    #     remaining_screenings = [screening for screening in screenings if screening.get_movie_id() != screening_id]
        
    #     if len(remaining_screenings) < len(screenings):
    #         FileUtility.write_to_file("screenings.txt", "\n".join([",".join([
    #             str(s.get_movie_id()),
    #             s.get_screeningDate().strftime("%Y-%m-%d"),
    #             s.get_startTime().strftime("%H:%M"),
    #             s.get_endTime().strftime("%H:%M"),
    #             str(s.get_hall())
    #         ]) for s in remaining_screenings]))
    #         return True
    #     return False

    # @classmethod
    # def get_screenings_by_times(cls, times: List[str]) -> List["Screening"]:
    #     all_screenings = cls.get_all_screenings()
    #     return [screening for screening in all_screenings if screening.get_startTime().strftime("%H:%M") in times]
    # def get_screenings_by_movie_title(cls, title: str) -> List["Screening"]:
    #     """
    #     Fetch all screenings for the given movie title.
    #     """
    #     all_screenings = cls.get_all_screenings()  # Using the existing method to get all screenings
    #     return [screening for screening in all_screenings if screening.get_movie_title() == title]


    # def get_schedule(self) -> str:
    #     date_str = self.__screeningDate.strftime("%Y-%m-%d")
    #     start_time_str = self.__startTime.strftime("%H:%M")
    #     end_time_str = self.__endTime.strftime("%H:%M")
    #     return f"{date_str} | {start_time_str} - {end_time_str} | Hall: {self.__hall}"

# class CinemaHall:
#     def __init__(self, hall_id: int, name: str, totalSeats: int):
#         self.__hall_id = hall_id
#         self.__name = name
#         self.__totalSeats = totalSeats
#         self.__listOfSeats = []

#     # Getters
#     def get_hall_id(self):
#         return self.__hall_id

#     def get_name(self):
#         return self.__name

#     def get_totalSeats(self):
#         return self.__totalSeats

#     def get_listOfSeats(self):
#         return self.__listOfSeats

#     # Setters
#     def set_name(self, name):
#         self.__name = name

#     def set_totalSeats(self, totalSeats):
#         self.__totalSeats = totalSeats

#     def set_listOfSeats(self, listOfSeats):
#         self.__listOfSeats = listOfSeats

    # @classmethod
    # def from_data(cls, data: str):
    #     """Create a CinemaHall instance from a comma-separated string."""
    #     hall_id, name, totalSeats = data.strip().split(',')
    #     return cls(int(hall_id), name, int(totalSeats))

    # @classmethod
    # def get_all_cinema_halls(cls):
    #     """Retrieve all cinema halls from the database."""
    #     data = FileUtility.read_from_file(cls.file_path)
    #     return [cls.from_data(hall) for hall in data]

    # @classmethod
    # def remove_cinema_hall(cls, hall_id: int):
    #     """Remove a cinema hall by its ID."""
    #     halls = cls.get_all_cinema_halls()
    #     remaining_halls = [hall for hall in halls if hall.get_hall_id() != hall_id]
    #     data = [f"{hall.get_hall_id()},{hall.get_name()},{hall.get_totalSeats()}" for hall in remaining_halls]
    #     FileUtility.write_to_file(cls.file_path, data)
    #     return len(halls) != len(remaining_halls)

    # file_path = "cinemahalls.txt"

# class CinemaHallSeat:
#     def __init__(
#         self,
#         seat_id: int,
#         hall_id: int,
#         seatNumber: int,
#         seatColumn: int,
#         seatType: int,
#         isReserved: bool,
#         seatPrice: float,
#     ):
#         self.__seat_id = seat_id
#         self.__hall_id = hall_id
#         self.__seatNumber = seatNumber
#         self.__seatColumn = seatColumn
#         self.__seatType = seatType
#         self.__isReserved = isReserved
#         self.__seatPrice = seatPrice

#     # Getters
#     def get_seat_id(self):
#         return self.__seat_id

#     def get_hall_id(self):
#         return self.__hall_id

#     def get_seatNumber(self):
#         return self.__seatNumber

#     def get_seatColumn(self):
#         return self.__seatColumn

#     def get_seatType(self):
#         return self.__seatType

#     def get_isReserved(self):
#         return self.__isReserved

#     def get_seatPrice(self):
#         return self.__seatPrice

#     # Setters
#     def set_seatNumber(self, seatNumber):
#         self.__seatNumber = seatNumber

#     def set_seatColumn(self, seatColumn):
#         self.__seatColumn = seatColumn

#     def set_seatType(self, seatType):
#         self.__seatType = seatType

#     def set_isReserved(self, isReserved):
#         self.__isReserved = isReserved

#     def set_seatPrice(self, seatPrice):
#         self.__seatPrice = seatPrice

    # @classmethod
    # def from_data(cls, data: str):
    #     """Create a CinemaHallSeat instance from a comma-separated string."""
    #     seat_id, hall_id, seatNumber, seatColumn, seatType, isReserved, seatPrice = map(int, data.strip().split(','))
    #     return cls(seat_id, hall_id, seatNumber, seatColumn, seatType, bool(isReserved), float(seatPrice))

    # @classmethod
    # def get_all_seats_for_hall(cls, hall_id: int):
    #     """Retrieve all seats for a specific cinema hall."""
    #     data = FileUtility.read_from_file(cls.file_path)
    #     return [cls.from_data(seat) for seat in data if int(seat.split(',')[1]) == hall_id]

    # @classmethod
    # def book_seat(cls, seat_id: int):
    #     """Mark a seat as booked."""
    #     seats = cls.get_all_seats()
    #     for seat in seats:
    #         if seat.get_seat_id() == seat_id:
    #             seat.set_isReserved(True)
    #             cls._save_all_seats(seats)
    #             return True
    #     return False

    # @classmethod
    # def unbook_seat(cls, seat_id: int):
    #     """Mark a seat as available."""
    #     seats = cls.get_all_seats()
    #     for seat in seats:
    #         if seat.get_seat_id() == seat_id:
    #             seat.set_isReserved(False)
    #             cls._save_all_seats(seats)
    #             return True
    #     return False

    # @classmethod
    # def get_all_seats(cls):
    #     """Helper method to get all seats irrespective of the hall."""
    #     data = FileUtility.read_from_file(cls.file_path)
    #     return [cls.from_data(seat) for seat in data]

    # @classmethod
    # def _save_all_seats(cls, seats: List["CinemaHallSeat"]):
    #     """Helper method to save all seats to the file."""
    #     data = []
    #     for seat in seats:
    #         seat_data = f"{seat.get_seat_id()},{seat.get_hall_id()},{seat.get_seatNumber()},{seat.get_seatColumn()},{seat.get_seatType()},{int(seat.get_isReserved())},{seat.get_seatPrice()}"
    #         data.append(seat_data)
    #     FileUtility.write_to_file(cls.file_path, data)

    # file_path = "cinemahallseats.txt"

# class Payment:
#     def __init__(self, amount: float, createdOn: datetime, paymentID: str):
#         self.__amount = amount
#         self.__createdOn = createdOn
#         self.__paymentID = paymentID
#         self.__coupon = None  # New attribute to hold the Coupon object

#     # Getter methods
#     def get_amount(self):
#         return self.__amount

#     def get_createdOn(self):
#         return self.__createdOn

#     def get_paymentID(self):
#         return self.__paymentID

#     def get_coupon(self) -> "Coupon":
#         return self.__coupon

#     # Setter methods
#     def set_amount(self, amount):
#         self.__amount = amount

#     def set_createdOn(self, createdOn):
#         self.__createdOn = createdOn

#     def set_paymentID(self, paymentID):
#         self.__paymentID = paymentID

#     def set_coupon(self, coupon: "Coupon"):
#         if coupon.get_expiryDate() > datetime.now():
#             self.__coupon = coupon
#         else:
#             print("Coupon has expired!")

    # @staticmethod
    # def make_payment(amount):
    #     """Make a payment and return the payment ID."""
        
    #     paymentID = "Trans" + str(len(FileUtility.read_from_file("Payment.txt")) + 1).zfill(3)
        
    #     # Write the payment details to Payment.txt using FileUtility
    #     payment_data = f"{amount},{str(datetime.date.today())},{paymentID}"
    #     FileUtility.append_to_file("Payment.txt", payment_data)
        
    #     return paymentID  # Return the payment ID to be linked to the booking



    # def calcDiscount(self) -> float:
    #     """Calculate the discount based on the coupon applied."""
    #     if self.__coupon:
    #         return self.__amount * (self.__coupon.get_discount() / 100)
    #     return 0

    # def calcFinalPayment(self) -> float:
    #     """Calculate the final payment after applying the discount."""
    #     discount = self.calcDiscount()
    #     return self.__amount - discount



# class Coupon:
#     def __init__(self, couponID: str, expiryDate: datetime, discount: float):
#         self.__couponID = couponID
#         self.__expiryDate = expiryDate
#         self.__discount = discount

#     # Getter methods
#     def get_couponID(self):
#         return self.__couponID

#     def get_expiryDate(self):
#         return self.__expiryDate

#     def get_discount(self):
#         return self.__discount

#     # Setter methods
#     def set_couponID(self, couponID):
#         self.__couponID = couponID

#     def set_expiryDate(self, expiryDate):
#         self.__expiryDate = expiryDate

#     def set_discount(self, discount):
#         self.__discount = discount

    # @classmethod
    # def fetch_all_coupons(cls):
    #     coupons = []
    #     lines = FileUtility.read_from_file('coupons.txt')
    #     for line in lines:
    #         data = line.split(',')
    #         couponID = data[0]
    #         expiryDate = datetime.strptime(data[1], "%Y-%m-%d")
    #         discount = float(data[2])
    #         coupons.append(Coupon(couponID, expiryDate, discount))
    #     return coupons

    # @classmethod
    # def add_coupon(cls, coupon):
    #     coupon_data = f"{coupon.get_couponID()},{coupon.get_expiryDate().strftime('%Y-%m-%d')},{coupon.get_discount()}"
    #     FileUtility.append_to_file('coupons.txt', coupon_data)

    # @classmethod
    # def update_coupon(cls, couponID, updated_coupon):
    #     coupons = cls.fetch_all_coupons()
    #     for index, coupon in enumerate(coupons):
    #         if coupon.get_couponID() == couponID:
    #             coupons[index] = updated_coupon
    #             break
    #     cls._overwrite_coupons_file(coupons)

    # @classmethod
    # def delete_coupon(cls, couponID):
    #     coupons = cls.fetch_all_coupons()
    #     coupons = [coupon for coupon in coupons if coupon.get_couponID() != couponID]
    #     cls._overwrite_coupons_file(coupons)

    # @classmethod
    # def _overwrite_coupons_file(cls, coupons):
    #     data = []
    #     for coupon in coupons:
    #         data.append(f"{coupon.get_couponID()},{coupon.get_expiryDate().strftime('%Y-%m-%d')},{coupon.get_discount()}")
    #     FileUtility.write_to_file('coupons.txt', "\n".join(data))

    # @classmethod
    # def fetch_coupon_by_id(cls, couponID):
    #     coupons = cls.fetch_all_coupons()
    #     for coupon in coupons:
    #         if coupon.get_couponID() == couponID:
    #             return coupon
    #     return None

# class Notification:
#     def __init__(self, notificationID: int, content: str):
#         self.__notificationID = notificationID
#         self.__createdOn = date.today()
#         self.__content = content

#     # Getter methods
#     def get_notificationID(self):
#         return self.__notificationID

#     def get_createdOn(self):
#         return self.__createdOn

#     def get_content(self):
#         return self.__content

#     # Setter methods
#     def set_notificationID(self, notificationID):
#         self.__notificationID = notificationID

#     def set_content(self, content):
#         self.__content = content

    # @classmethod
    # def fetch_all_notifications(cls):
    #     notifications = []
    #     lines = FileUtility.read_from_file('notifications.txt')
    #     for line in lines:
    #         data = line.split(',')
    #         notificationID = int(data[0])
    #         createdOn = datetime.strptime(data[1], "%Y-%m-%d").date()
    #         content = data[2]
    #         notifications.append(Notification(notificationID, content))
    #     return notifications

    # def save(self):
    #     notification_data = f"{self.get_notificationID()},{self.get_createdOn().strftime('%Y-%m-%d')},{self.get_content()}"
    #     FileUtility.append_to_file('notifications.txt', notification_data)

    # @staticmethod
    # def send_notification(user, message):
    #     # Here, you can modify this method to handle how you want to send/display the notifications
    #     print(f"Notification to {user}: {message}")
        
    #     # Saving the notification after sending
    #     notificationID = len(FileUtility.read_from_file('notifications.txt')) + 1
    #     notification = Notification(notificationID, message)
    #     notification.save()

# # class Booking:
# #     file_path = "bookings.txt"
    
# #     def __init__(self, booking_id, username, movie_name, date, screening_id, seats, amount, payment_id):
# #         self._booking_id = booking_id
# #         self._username = username
# #         self._movie_name = movie_name
# #         self._date = date
# #         self._screening_id = screening_id
# #         self._seats = seats
# #         self._amount = amount
# #         self._payment_id = payment_id
# #         self.__notifications = []

# #     # Getters and Setters for booking_id
# #     @property
# #     def booking_id(self):
# #         return self._booking_id

# #     # Getters and Setters for username
# #     @property
# #     def username(self):
# #         return self._username
    
# #     @username.setter
# #     def username(self, value):
# #         self._username = value

# #     # Getters and Setters for movie_name
# #     @property
# #     def movie_name(self):
# #         return self._movie_name
    
# #     @movie_name.setter
# #     def movie_name(self, value):
# #         self._movie_name = value

# #     # Getters and Setters for date
# #     @property
# #     def date(self):
# #         return self._date
    
# #     @date.setter
# #     def date(self, value):
# #         self._date = value

# #     # Getters and Setters for screening_id
# #     @property
# #     def screening_id(self):
# #         return self._screening_id
    
# #     @screening_id.setter
# #     def screening_id(self, value):
# #         self._screening_id = value

# #     # Getters and Setters for seats
# #     @property
# #     def seats(self):
# #         return self._seats
    
# #     @seats.setter
# #     def seats(self, value):
# #         self._seats = value

# #     # Getters and Setters for amount
# #     @property
# #     def amount(self):
# #         return self._amount
    
# #     @amount.setter
# #     def amount(self, value):
# #         self._amount = value

# #     # Getters and Setters for payment_id
# #     @property
# #     def payment_id(self):
# #         return self._payment_id
    
# #     @payment_id.setter
# #     def payment_id(self, value):
# #         self._payment_id = value

# #     # Getters and Setters for notifications
# #     @property
# #     def notifications(self):
# #         return self.__notifications

# #     @notifications.setter
# #     def notifications(self, value):
# #         self.__notifications = value

#     @classmethod
#     def get_all_bookings(cls):
#         """Retrieve all bookings from the database."""
#         return FileUtility.read_from_file(cls.file_path)
    
#     @classmethod
#     def get_booking_by_id(cls, booking_id):
#         """Retrieve a booking by its ID."""
#         bookings = cls.get_all_bookings()
#         return next((booking for booking in bookings if booking.split(",")[0] == booking_id), None)
    
#     @classmethod
#     def get_all_bookings_for_user(cls, username):
#         """Retrieve all bookings for a specific user from the database."""
#         all_bookings = cls.get_all_bookings()
#         user_bookings = [booking for booking in all_bookings if booking.username == username]
#         return user_bookings
    
#     @classmethod
#     def create(cls, customer_username, movie_title, screening_time, seats, payment_method, coupon=None):
#         # Retrieve the movie and screening details
#         movie = Movie.search_movies(title=movie_title)[0]
#         screening = [s for s in movie.get_screenings() if s.get_schedule() == screening_time][0]
        
#         # Use the customer's username to retrieve the customer object
#         customer = next((user for user in User.get_all_users() if user.get_username() == customer_username), None)
#         if not isinstance(customer, Customer):
#             raise ValueError("Invalid customer username provided.")
        
#         # Check if seats are available for the given screening
#         if not screening.are_seats_available(seats):
#             return False
        
#         # Calculate the total price for the seats
#         total_price = screening.get_price_for_seats(seats)
        
#         # Create a new booking instance
#         booking_id = f"BK{len(FileUtility.read_from_file(cls.file_path)) + 1:04}"  # Sample format: BK0001
#         booking = Booking(booking_id, customer.username, movie.title, screening.get_date(), screening.screening_id, seats, total_price, None)
        
#         # Apply discount if coupon is provided
#         if coupon:
#             booking.amount -= (booking.amount * coupon.get_discount() / 100)
#             # Ensure amount doesn't go negative
#             booking.amount = max(0, booking.amount)
        
#         # Payment processing (for simplicity, we'll just print a message)
#         print(f"Payment of {booking.amount} received via {payment_method}.")
        
#         # Save the booking to the bookings.txt database
#         booking_details = ",".join([
#             booking.booking_id,
#             booking.username,
#             booking.movie_name,
#             str(booking.date),
#             booking.screening_id,
#             '-'.join(booking.seats),  # Using '-' to join seats into a single string
#             str(booking.amount),
#             booking.payment_id or "N/A"  # Using "N/A" if payment_id is None
#         ])
#         FileUtility.append_to_file(cls.file_path, booking_details)
        
#         return True

     
#     @classmethod
#     def remove_booking(cls, booking_id):
#         """Remove a booking by its ID."""
#         bookings = cls.get_all_bookings()
#         booking = cls.get_booking_by_id(booking_id)
#         if booking:
#             bookings.remove(booking)
#             FileUtility.write_to_file(cls.file_path, bookings)
#             return True
#         return False
    
#     @classmethod
#     def refund_for_canceled_screening(cls, screening_id: str) -> List[str]:
#         bookings = cls.get_all_bookings()
#         affected_bookings = [booking for booking in bookings if booking.split(",")[4] == screening_id]
        
#         for booking in affected_bookings:
#             booking_id = booking.split(",")[0]
#             cls.remove_booking(booking_id)
            
#         return affected_bookings
    
#     def add_notification(self, notification: Notification):
#         self.__notifications.append(notification)

#     def get_notifications(self):
#         return self.__notifications

#     @classmethod
#     def display_seats(cls, screening_id):
#         seats = CinemaHallSeat.get_all_seats_for_hall(screening_id)
#         for seat in seats:
#             print(seat)

#     @classmethod
#     def book_seats(cls, screening_id, seat_positions):
#         for seat_id in seat_positions:
#             CinemaHallSeat.book_seat(seat_id)
#         return "Seats booked successfully!"
    
#     @classmethod
#     def apply_discount(cls, coupon_code):
#         # Fetch all coupons from the file
#         all_coupons = Coupon.fetch_all_coupons()
        
#         matching_coupon = next((coupon for coupon in all_coupons if coupon.get_couponID() == coupon_code), None)
        
#         if matching_coupon and matching_coupon.get_expiryDate() > datetime.now().date():
#             discount_percentage = matching_coupon.get_discount()
#             return discount_percentage
        
#         return 0.0



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

    # Getter for booking list
    def getBookingList(self) -> List[Booking]:
        return self.__bookingList

    # Setter for booking list
    def setBookingList(self, bookingList: List[Booking]):
        self.__bookingList = bookingList

    # Getter for notifications
    def get_notifications(self) -> List[str]:
        return self.__notificationList

    # Setter for notifications
    def set_notifications(self, notifications: List[str]):
        self.__notificationList = notifications

    def search_movies(self, title=None, language=None, genre=None, release_date=None) -> List[Movie]:
        return Movie.search_movies(title, language, genre, release_date)

    def makeBooking(self, screening: Screening, seats: List[str], coupon: Optional[Coupon] = None) -> bool:
        booking = Booking.create(
            self.username,
            screening,
            seats,
            coupon
        )
        
        if not booking:
            self.add_notification(f"Booking failed for movie {screening.get_movie().get_title()} on date {screening.get_date()}.")
            return False
        
        self.__bookingList.append(booking)
        self.add_notification(f"Booking successful for movie {screening.get_movie().get_title()} on date {screening.get_date()}.")
        return True

    def add_coupon(self, coupon_code: str) -> bool:
        all_coupons = Coupon.fetch_all_coupons()
        matching_coupon = next((coupon for coupon in all_coupons if coupon.get_couponID() == coupon_code), None)
        
        if matching_coupon and matching_coupon.get_expiryDate() > datetime.date.today():
            self.__coupon = matching_coupon
            return True
        
        self.add_notification("Invalid or expired coupon.")
        return False

    def cancelBooking(self, booking_id: str) -> bool:
        booking_to_cancel = next((booking for booking in self.__bookingList if booking.booking_id == booking_id), None)
            
        if booking_to_cancel:
            self.__bookingList.remove(booking_to_cancel)
            Booking.remove_booking(booking_id)
            
            self.add_notification(f"Booking {booking_id} for movie {booking_to_cancel.movie_name} on date {booking_to_cancel.date} has been canceled.")
            return True
            
        return False

    # Add a notification
    def add_notification(self, message: str):
        self.__notificationList.append(message)
