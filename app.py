from flask import session
from datetime import datetime,date
from model.db import database_execute_query_fetchone, database_execute_query_fetchall,database_execute_action,database_execute_lastrowid
from typing import List,Dict, Any, Optional
from flask import abort, session,flash
import model.user, model.booking,model.cinema_hall,model.cinema_hall_seats,model.coupon,model.movie,model.notification,model.payment,model.screening,model.utilities
import json
import mysql.connector
import sqlite3

# Your code here



class GeneralController:
    
   
    def searchMovieTitle(title: str) -> List[model.movie.Movie]:
        all_movies = MovieController.search_movie_by_title()
        return all_movies
    
    def searchMovieLanguage(language: str) -> List[model.movie.Movie]:
        all_movies = MovieController.search_movie_by_language()
        return all_movies

    
    def searchMovieGenre(genre: str) -> List[model.movie.Movie]:
        all_movies = MovieController.search_movie_by_genre()
        return all_movies

   
    def searchMovieDate(rDate: datetime) -> List[model.movie.Movie]:
        all_movies = MovieController.search_movie_by_date()
        return all_movies
    
    def viewMovieDetails(movie_id):
        movie_details= MovieController.get_movie_by_id(movie_id)
        return movie_details

class UserController(GeneralController):
   
    

    @staticmethod
    def get_user_role(username: str) -> str:
        query = "SELECT Type FROM Users WHERE Username = %s"
        result = database_execute_query_fetchone(query, (username,))
        return result["Type"] if result else None

    @staticmethod
    def is_logged_in() -> bool:
        """Check if there is a session for the user."""
        return "username" in session and "Type" in session

    @staticmethod
    def auth_handler(role_list: list) -> bool:
        """Check if the user is logged in and if the user's role is in the role list."""
        if UserController.is_logged_in():
            if session["Type"] not in role_list:
                
                abort(403)
           
            return True
        else:
            
            return False



    def login(username: str, password: str) -> bool:
        query = "SELECT * FROM Users WHERE Username = %s"
        params = (username,)
        user_record = database_execute_query_fetchone(query, params)
        
        if user_record and user_record['Password'] == password:  
            session['logged_in'] = True
            session['username'] = username
            session['user_id'] = user_record['ID'] 
            session['type']=user_record['Type']
            return True
        else:
            return False

    
    def logout() -> bool:
        session.clear() 
        return True
    @staticmethod
    def email_exists(email: str) -> bool:
        query = "SELECT 1 FROM Users WHERE Email = %s"
        params = (email,)
        result = database_execute_query_fetchone(query, params)
        return result is not None

    @staticmethod
    def username_exists(username: str) -> bool:
        query = "SELECT 1 FROM Users WHERE Username = %s"
        params = (username,)
        result = database_execute_query_fetchone(query, params)
        return result is not None

    
    @staticmethod
    def add_user(name: str, address: str, email: str, phone: str, username: str, password: str, user_type: str) -> tuple[bool, str]:
        # Check if email already exists in the database
        if UserController.email_exists(email):
            flash("Email already registered.")
            return False, "Email already registered."

        # Check if username already exists in the database
        if UserController.username_exists(username):
            flash("Username already taken.")
            return False, "Username already taken."

        query = """
            INSERT INTO Users (Name, Address, Email, Phone, Username, Password, Type) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        params = (name, address, email, phone, username, password, user_type)
        try:
            result=database_execute_lastrowid(query, params)
            return True, result
        except mysql.connector.IntegrityError as e:
            if '1062' in str(e):
                return False, "Email or Username already exists."
            else:
                return False, str(e)
        except Exception as e:
            return False, str(e)

    @staticmethod
    def update_password(username: str, new_password: str) -> bool:
        query = "UPDATE Users SET Password = %s WHERE Username = %s"
        params = (new_password, username)
        return database_execute_action(query, params)
    
    @staticmethod
    def get_user_id_from_username(username: str) -> Optional[int]:
        
        query = "SELECT ID FROM Users WHERE Username=%s"
        params = (username,)
        record = database_execute_query_fetchone(query, params)
        if record:
            return record['ID']
        return None

class AdminController(UserController):
   
    def addMovie(title, language, genre, releaseDate, duration, rating, description, poster):
        return MovieController.add_movie(title, language, genre, releaseDate, duration, rating, description, poster)
    def addScreening(movie_id, date, time, cinema_hall_id):
        return ScreeningController.add_screening(movie_id, date, time, cinema_hall_id)
    def cancelMovie(movie_id):
        return MovieController.remove_movie(movie_id)
    def cancelScreening(screening_id):
        return ScreeningController.remove_screening(screening_id)
   
class FrontDeskStaffController(UserController):
    def makeBooking():
        return BookingController.create()
    def cancelBooking(booking_id):
        return BookingController.remove_booking(booking_id)
    
    def makePayment(amount):
        return PaymentController.make_payment(amount)
    def applyCoupon(coupon_code):
        return CouponController.apply_coupon(coupon_code)
    def bookSeat(seat_id):
        return CinemaHallSeatController.book_seat(seat_id)
    def unbookSeat(seat_id):
        return CinemaHallSeatController.unbook_seat(seat_id)
    
    
class CustomeController(UserController):
    def makeBooking():
        return BookingController.create()
    def cancelBooking(booking_id):
        return BookingController.remove_booking(booking_id)
    def checkBooking(booking_id):
        return BookingController.get_booking_by_id(booking_id)
    def bookSeat(seat_id):
        return CinemaHallSeatController.book_seat(seat_id)
    def unbookSeat(seat_id):
        return CinemaHallSeatController.unbook_seat(seat_id)
    def viewMovieDetails(movie_id):
        return super().viewMovieDetails()
    def makePayment(amount):
        return PaymentController.make_payment(amount)
    def applyCoupon(coupon_code):
        return CouponController.apply_coupon(coupon_code)
    
    
class GuestController(UserController):
    def register(self):
        return UserController.add_user()

class CinemaHallController:
    
    @staticmethod
    def get_all_cinema_halls() -> List[Dict[str, str]]:
        """Retrieve all cinema halls from the database."""
        query = "SELECT * FROM CinemaHalls"
        return database_execute_query_fetchall(query)

    @staticmethod
    def get_all_screenings_by_hall_id(hall_id: int) -> List[Dict[str, str]]:
        """Retrieve all screenings for a given cinema hall ID."""
        query = """
            SELECT * FROM Screenings
            WHERE HallID = %s
        """
        return database_execute_query_fetchall(query, (hall_id,))
    @staticmethod
    def get_hall_details(hall_id: int) -> Dict[str, Any]:
        query = "SELECT * FROM CinemaHalls WHERE ID = %s"
        params = (hall_id,)
        result = database_execute_query_fetchall(query, params)
        

        if result:
            hall = result[0]
            details = {
                'id': hall['ID'],
                'name': hall['Name'], 
                'total_seats': hall['TotalSeats']  
            }
            return details
        return None


class MovieController:
    @staticmethod
    def search_movies_by_keywords(keywords: str) -> List[model.movie.Movie]:
        query = """
        SELECT *
        FROM Movies
        WHERE
            Title LIKE %s OR
            Director LIKE %s OR
            Genre LIKE %s OR
            Description LIKE %s OR
            Language LIKE %s OR
            Country LIKE %s OR
            Director LIKE %s 
        """
        
        params = ['%' + keywords + '%'] * 7
        result = database_execute_query_fetchall(query, params)
        
       
        movies = []
        for row in result:
            movie = model.movie.Movie(
                title=row['Title'],
                description=row['Description'],
                durationMins=row['DurationMins'],
                language=row['Language'],
                releaseDate=row['ReleaseDate'],
                director=row['Director'],
                country=row['Country'],
                genre=row['Genre'],
                movie_id=row['ID']
                
               
            )
            movies.append(movie)
        
        return movies
    
    @staticmethod
    def search_movie_by_language(language: str) -> List[model.movie.Movie]:
        
        
        query = "SELECT * FROM Movies WHERE Language = %s"
        records=database_execute_query_fetchall(query, (language,))
        
        
        movies = []
        for record in records:
            movie =model.movie.Movie(title=record['Title'], 
                        description=record['Description'], 
                        durationMins=record['DurationMins'], 
                        language=record['Language'], 
                        releaseDate=record['ReleaseDate'], 
                        country=record['Country'], 
                        genre=record['Genre'], 
                        movie_id=record['ID'])
            movies.append(movie)

        return movies

    def search_movie_by_genre(genre: str) -> List[model.movie.Movie]:
       
        
        query = "SELECT * FROM Movies WHERE Genre = %s"
        records=database_execute_query_fetchall(query, (genre,))

        movies = []
        for record in records:
            movie = model.movie.Movie(title=record['Title'], 
                        description=record['Description'], 
                        durationMins=record['DurationMins'], 
                        language=record['Language'], 
                        releaseDate=record['ReleaseDate'], 
                        country=record['Country'], 
                        genre=record['Genre'], 
                        movie_id=record['ID'])
            movies.append(movie)

        return movies

    def search_movie_by_date(releaseDate: datetime) -> List[model.movie.Movie]:
        
        
        query = "SELECT * FROM Movies WHERE ReleaseDate = %s"
        records = database_execute_query_fetchall(query, (releaseDate,))     
        

        movies = []
        for record in records:
            movie = model.movie.Movie(title=record['Title'], 
                        description=record['Description'], 
                        durationMins=record['DurationMins'], 
                        language=record['Language'], 
                        releaseDate=record['ReleaseDate'], 
                        country=record['Country'], 
                        genre=record['Genre'], 
                        movie_id=record['ID'])
            movies.append(movie)

        return movies

    def search_movie_by_title(title: str) -> List[model.movie.Movie]:
       
        query = "SELECT * FROM Movies WHERE Title LIKE %s"
        title_pattern = "%" + title + "%"        
        records = database_execute_query_fetchall(query, (title_pattern,))       
        

        movies = []
        for record in records:
            movie = model.movie.Movie(title=record['Title'], 
                        description=record['Description'], 
                        durationMins=record['DurationMins'], 
                        language=record['Language'], 
                        releaseDate=record['ReleaseDate'], 
                        country=record['Country'], 
                        genre=record['Genre'], 
                        movie_id=record['ID'])
            movies.append(movie)

        return movies

    

    def add_movie(title: str, description: str, durationMins: int, language: str, releaseDate: datetime.date, country: str, genre: str) -> bool:
        query = """
        INSERT INTO Movies (Title, Description, DurationMins, Language, ReleaseDate, Country, Genre)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        params = (title, description, durationMins, language, releaseDate, country, genre)
        try:
            database_execute_action(query, params)
            return True
        except:
            return False
        
    @staticmethod
    def remove_movie(movie_id: int) -> (bool, str):
        # Check if there are any screenings for this movie
        screenings = ScreeningController.get_screening_by_movie_id(movie_id)
        if screenings:
            return False, "There are screenings associated with this movie."

        query = "DELETE FROM Movies WHERE ID = %s"
        params = (movie_id,)

        try:
            return database_execute_action(query, params), "Movie deleted."
        except Exception as e:
            # Handle specific database exceptions if needed
            return False, f"An error occurred: {e}"

    def get_all_movies() -> List[model.movie.Movie]:
        query = "SELECT * FROM movies"
        records = database_execute_query_fetchall(query)
        movies = []
        for record in records:
            movie = model.movie.Movie(title=record['Title'],
                                      description=record['Description'],
                                      durationMins=record['DurationMins'],
                                      language=record['Language'],
                                      releaseDate=record['ReleaseDate'],
                                      director=record['Director'],
                                      country=record['Country'],
                                      genre=record['Genre'],
                                      movie_id=record['ID']                                     
                                      )
            movies.append(movie.get_details())
        return movies

    def get_movie_by_id(movie_id: int) -> Optional[model.movie.Movie]:
        query = "SELECT * FROM Movies WHERE ID = %s"
        params = (movie_id,)
        record = database_execute_query_fetchone(query, params)
        if record:
            return model.movie.Movie(title=record['Title'],
                                     description=record['Description'],
                                     durationMins=record['DurationMins'],
                                     language=record['Language'],
                                     releaseDate=record['ReleaseDate'],
                                     director=record['Director'],
                                     country=record['Country'],
                                     genre=record['Genre'],
                                     movie_id=record['ID']
                                     )
        return None

    def view_details_by_id(movie_id: int) -> Optional[dict]:
        movie = MovieController.get_movie_by_id(movie_id)
        if movie:
            return model.movie.Movie.get_details()
        return None
    
    def get_screenings(movie_id: int) -> List[model.screening.Screening]:
        query = """
        SELECT * FROM Screenings
        WHERE MovieID = %s
        """
        params = (movie_id,)
        records = database_execute_query_fetchall(query, params)
        
        screenings = []
        for record in records:
            screening = model.screening.Screening(screening_id=record['ID'],
                                                  movie_id=record['MovieID'],
                                                  screening_date=record['ScreeningDate'],
                                                  start_time=record['StartTime'],
                                                  end_time=record['EndTime'],
                                                  hall_id=record['HallID'])
            screenings.append(screening)
        return screenings

class NotificationController:
    @staticmethod
    def create_notification(user_id: int, message: str) -> bool:
        """
        Creates a new notification.

        Args:
        - user_id (int): ID of the user for whom the notification is intended.
        - message (str): The notification message.

        Returns:
        - bool: True if notification was successfully created, False otherwise.
        """
        query = "INSERT INTO Notifications (UserID, Message) VALUES (%s, %s)"
        params = (user_id, message)
        
        return database_execute_action(query, params)

    
    @staticmethod
    def mark_notification_read(notification_id: int) -> bool:
        """
        Marks a specific notification as read.

        Args:
        - notification_id (int): ID of the notification to be marked as read.

        Returns:
        - bool: True if the operation was successful, False otherwise.
        """
        query = "UPDATE Notifications SET IsRead=1 WHERE ID=%s"
        params = (notification_id,)
        
        return database_execute_action(query, params)

    @staticmethod
    def mark_notification_unread(notification_id: int) -> bool:
        """
        Marks a specific notification as unread.

        Args:
        - notification_id (int): ID of the notification to be marked as unread.

        Returns:
        - bool: True if the operation was successful, False otherwise.
        """
        query = "UPDATE Notifications SET IsRead=0 WHERE ID=%s"
        params = (notification_id,)
        
        return database_execute_action(query, params)

class PaymentController:

    @staticmethod
    def get_coupon_details_by_code(coupon_code):
        query = "SELECT * FROM Coupons WHERE CouponCode = %s"
        result = database_execute_query_fetchall(query, (coupon_code,))
        return result[0] if result else None



    @staticmethod
    def make_payment(amount: float, coupon_id: Optional[int] = None) -> Optional[int]:
        """
        Makes a payment and returns the payment ID.

        Args:
        - amount (float): The payment amount.
        - coupon_id (int, optional): The coupon ID if a coupon is used.

        Returns:
        - Optional[int]: The payment ID after successful payment or None if failed.
        """
        try:
            query = "INSERT INTO Payments (Amount, CreatedOn, CouponID) VALUES (%s, CURDATE(), %s)"
            params = (amount, coupon_id)
            

            # Execute the insert query and get the last row id
            payment_id = database_execute_lastrowid(query, params)
           

            return payment_id
        except Exception as e:
            
            return None
        
    @staticmethod
    def update_payment_and_status_for_booking(booking_id: int, payment_id: int, status: str) -> bool:
        """
        Update the payment ID and status for a specific booking.

        """
        query = """
            UPDATE Bookings
            SET PaymentID = %s, Booking_Status = %s
            WHERE ID = %s
        """
        params = (payment_id, status, booking_id)
        try:
            database_execute_action(query, params)
            return True
        except Exception as e:
            print(f"Error updating payment and status for booking_id {booking_id}: {e}")
            return False

    @staticmethod
    def get_payment_id(booking_id: int) -> Optional[int]:
        query = "SELECT PaymentID FROM Bookings WHERE ID = %s"
        params = (booking_id,)
        record = database_execute_query_fetchone(query, params)
        if record:
            return record['PaymentID']
        return None

 

    @staticmethod
    def refund_payment(payment_id):
        try:
            
            query = "UPDATE Payments SET Refunded = 1 WHERE ID = %s"
            
            database_execute_action(query, (payment_id,))
            
            
        
        except Exception as e:
           
           print("An error occurred while refunding the payment: " + str(e), "error")

    
    
    
    @staticmethod
    def get_total_due(booking_id: int) -> float:
        """Get the total amount due for a particular booking."""
        query = """
            SELECT SUM(SeatPrice) AS total_due
            FROM Booked_Seats
            JOIN CinemaHallSeats ON Booked_Seats.Seat_ID = CinemaHallSeats.ID
            WHERE Booked_Seats.BookingID = %s
        """
        result = database_execute_query_fetchone(query, (booking_id,))
        

        if result is not None and 'total_due' in result:
            
            return result['total_due']
        else:
           
            return 0.0




class ScreeningController:


    @staticmethod
    def get_all_screenings() -> List[model.screening.Screening]:
        query = """
        SELECT Screenings.ID, Screenings.MovieID, Screenings.ScreeningDate, 
            Screenings.StartTime, Screenings.EndTime, Screenings.HallID,
            CinemaHalls.Name AS HallName
        FROM Screenings
        JOIN CinemaHalls ON Screenings.HallID = CinemaHalls.ID
        """
        records = database_execute_query_fetchall(query)
        
        screenings = []
        for record in records:
            screening = model.screening.Screening(
                    screeningDate=record['ScreeningDate'],
                    startTime=record['StartTime'],
                    endTime=record['EndTime'],
                    hall_id=record['HallID'],
                    hall_name=record['HallName'],  # Make sure this matches the alias in the SQL query
                    movie_id=record['MovieID'],                    
                    screening_id=record['ID']
                )

            screening_details = screening.get_details()
            screenings.append(screening_details)
        return screenings
   

    @staticmethod
    def get_screening_by_id(screening_id: int):
        query = "SELECT * FROM Screenings WHERE screening_id = %s"
        params = (screening_id, )
        result = database_execute_query_fetchone(query, params)
        if result:
          
            screening = model.screening.Screening(
                screening_id=result['screening_id'],
                movie_id=result['movie_id'],
                hall_id=result['hall_id'],
                screeningDate=result['screeningDate'],
                startTime=result['startTime'],
                endTime=result['endTime'],
                hall_name=result['hall_name'],
              
            )
            return screening
        else:
            return None

    
    @staticmethod
    def get_screening_by_movie_id(movie_id: int) -> List[model.screening.Screening]:
        query = """
        SELECT s.*, h.Name 
        FROM Screenings s
        INNER JOIN CINEMAHALLS h ON s.HallID = h.ID
        WHERE s.MovieID = %s
        """
        params = (movie_id,)
        records = database_execute_query_fetchall(query, params)
        
        screenings = []
        for record in records:
            screening = model.screening.Screening(
                    screeningDate=record['ScreeningDate'],
                    startTime=record['StartTime'],
                    endTime=record['EndTime'],
                    hall_id=record['HallID'],                      
                    movie_id=record['MovieID'],
                    screening_id=record['ID'],
                    hall_name=record['Name']
                )
            screen_details=screening.get_details()
            screenings.append(screen_details)
        return screenings
    
    @staticmethod
    def get_movie_id_by_screening(screening_id: int) -> int:
        query = """
        SELECT MovieID FROM Screenings
        WHERE ID = %s
        """
        params = (screening_id,)
        # record = database_execute_query_fetchone(query, params)
        
        # if record:
        #     return record['MovieID']
        # else:
        #     return None
        try:
            record = database_execute_query_fetchone(query, params)
            if record:
                return record['MovieID']
            else:
                return None
        except Exception as e:
            print(f"Error fetching movie_id for screening_id {screening_id}: {e}")
            return None


    @staticmethod
    def get_screening_by_movie_title(movie_title: str) -> List[model.screening.Screening]:
        query = """
        SELECT s.* FROM Screenings s
        INNER JOIN Movies m ON s.MovieID = m.ID
        WHERE m.Title = %s
        """
        params = (movie_title,)
        records = database_execute_query_fetchall(query, params)
        
        screenings = []
        for record in records:
            screening = model.screening.Screening(screening_id=record['ID'],
                                                  movie_id=record['MovieID'],
                                                  screening_date=record['ScreeningDate'],
                                                  start_time=record['StartTime'],
                                                  end_time=record['EndTime'],
                                                  hall_id=record['HallID'])
            screen_details=screening.get_details()
            screenings.append(screen_details)
        return screenings
    
    @staticmethod
    def get_screenings_by_hall(hall_id: int) -> List[Dict[str, Any]]:
        """Retrieve all screenings for a given hall ID."""
        query = """
            SELECT * FROM Screenings
            WHERE HallID = %s
        """
        return database_execute_query_fetchall(query, (hall_id,))

    

    @staticmethod
    def add_screening(screening: model.screening.Screening) -> bool:
        query = """
        INSERT INTO Screenings (MovieID, ScreeningDate, StartTime, EndTime, HallID)
        VALUES (%s, %s, %s, %s, %s)
        """
        params = (
            screening.get_movie_id(),
            screening.get_screeningDate(),
            screening.get_startTime(),
            screening.get_endTime(),
            screening.get_hall_id()
        )
        
        last_row_id = database_execute_lastrowid(query, params)
        return last_row_id > 0  

    
    @staticmethod
    def remove_screening(screening_id: int) -> (bool, str):
        # First, check if there are any booked seats for the screening
        check_query = "SELECT COUNT(*) as count FROM booked_seats WHERE ScreeningID = %s"
        booked_seats_result = database_execute_query_fetchone(check_query, (screening_id,))
        
        if booked_seats_result and booked_seats_result['count'] > 0:
            # If there are booked seats, do not delete and return a message
            return False, "Cannot delete the screening because there are booked seats."

        # If there are no booked seats, proceed to delete the screening
        delete_query = "DELETE FROM Screenings WHERE ID = %s"
        delete_success = database_execute_action(delete_query, (screening_id,))

        if delete_success:
            return True, "Screening successfully deleted."
        else:
            return False, "An error occurred while trying to delete the screening."




    # @staticmethod
    # def remove_screening(screening_id: int) -> bool:
    #     query = """
    #     DELETE FROM Screenings WHERE ID = %s
    #     """
    #     params = (screening_id,)
    #     return database_execute_action(query, params)

    @staticmethod
    def update_screening(screening: model.screening.Screening) -> bool:
        query = """
        UPDATE Screenings 
        SET MovieID = %s, ScreeningDate = %s, StartTime = %s, EndTime = %s, HallID = %s
        WHERE ID = %s
        """
        params = (screening.get_movie_id(), screening.get_screeningDate(), screening.get_startTime(), screening.get_endTime(), screening.get_hall_id(), screening.get_screening_id())
        return database_execute_action(query, params)
    

    @staticmethod
    def get_screening_details(screening_id: int) -> Dict[str, Any]:
        query = """
        SELECT 
            s.ID, 
            s.MovieID, 
            s.ScreeningDate, 
            s.StartTime, 
            s.EndTime, 
            s.HallID, 
            m.Title AS MovieTitle 
        FROM Screenings s
        JOIN Movies m ON s.MovieID = m.ID
        WHERE s.ID = %s
        """
        params = (screening_id,)
        result = database_execute_query_fetchall(query, params)
        
        if result:
            # Convert the result tuple to a dictionary for easier use in the template
            details = {
                'id': result[0]['ID'],
                'movie_id': result[0]['MovieID'],
                'movie_title': result[0]['MovieTitle'],  # Added movie title here
                'date': result[0]['ScreeningDate'],
                'start_time': result[0]['StartTime'],
                'end_time': result[0]['EndTime'],
                'hall_id': result[0]['HallID'],
            }
            return details
        return None




class CinemaHallSeatController:
    
    @staticmethod
    def get_all_seats_for_hall(hall_id: int) -> List[Dict[str, str]]:
        """Retrieve all seats for a given cinema hall ID."""
        query = """
            SELECT * FROM CinemaHallSeats
            WHERE HallID = %s
        """
        return database_execute_query_fetchall(query, (hall_id,))

    # @staticmethod
    # def book_seat(screening_id, selected_seats):
    #     parsed_seats = CinemaHallSeatController.parse_selected_seats(selected_seats)

    #     # Ensure parsed_seats is a list
    #     if not isinstance(parsed_seats, list):
    #         parsed_seats = [parsed_seats]

    #     # Assuming parsed_seats are always integers because they come from JSON parsing
    #     valid_seats = [str(seat) for seat in parsed_seats]  # Convert to string if necessary

    #     # Now valid_seats should be a list of strings
    #     valid_seats = [seat for seat in valid_seats if seat.isdigit()]

    #     if not valid_seats:
    #         raise ValueError("No valid seat IDs provided.")

    #     # Create the placeholders and params for the SQL query
    #     placeholders = ', '.join(['(%s, %s)'] * len(valid_seats))
    #     params = []
    #     for seat in valid_seats:
    #         params.extend((screening_id, seat))

    #     query = f"INSERT INTO booked_seats (ScreeningID, Seat_ID) VALUES {placeholders}"

    #     # Execute the insert statement with all parameters
    #     database_execute_action(query, params)
    @staticmethod
    def book_seat(screening_id, selected_seats, booking_id):
        # Ensure selected_seats is a list of strings
        if not isinstance(selected_seats, list):
            selected_seats = [selected_seats]

        # Filter out any non-digit strings just to be safe
        valid_seats = [seat for seat in selected_seats if seat.isdigit()]

        if not valid_seats:
            raise ValueError("No valid seat IDs provided.")

        # Create the placeholders and params for the SQL query
        placeholders = ', '.join(['(%s, %s, %s)'] * len(valid_seats))
        params = []
        for seat in valid_seats:
            params.extend((screening_id, seat, booking_id))  # Add booking_id to the parameters

        query = f"INSERT INTO booked_seats (ScreeningID, Seat_ID, BookingID) VALUES {placeholders}"
       

        
        database_execute_action(query, params)



    @staticmethod
    def unbook_seat(screening_id: int, seat_id: int) -> bool:
        """Remove a seat from the Booked_Seats table."""
        query = """
            DELETE FROM Booked_Seats WHERE ScreeningID = %s AND Seat_ID = %s
        """
        return database_execute_action(query, (screening_id, seat_id))


    @staticmethod
    def get_available_seats_for_hall(hall_id: int) -> List[Dict[str, str]]:
        """Get all unreserved seats for a given cinema hall ID."""
        query = """
            SELECT * FROM CinemaHallSeats
            WHERE HallID = %s AND ReservedStatus = FALSE
        """
        return database_execute_query_fetchall(query, (hall_id,))
    
    @staticmethod
    def get_booked_seats_for_hall(hall_id: int) -> List[str]:
        """Retrieve all booked seats for a given hall."""
        query = """
            SELECT Seat_ID
            FROM Booked_Seats
            JOIN Screenings ON Booked_Seats.ScreeningID = Screenings.ID
            WHERE Screenings.HallID = %s
        """
        results = database_execute_query_fetchall(query, (hall_id,))
        booked_seats = [result['Seat_ID'] for result in results]
        return booked_seats


    @staticmethod
    def get_seat_price(seat_id: int) -> float:
        """Retrieve the price of a specific seat."""
        query = """
            SELECT SeatPrice FROM CinemaHallSeats
            WHERE ID = %s
        """
        result = database_execute_query_fetchall(query, (seat_id,))
        return result[0]['SeatPrice'] if result else 0

    @staticmethod
    def get_booked_seats_total_price(seat_ids: List[int]) -> float:
        """Compute the total price for a list of booked seats."""
        query = f"""
            SELECT SUM(SeatPrice) AS total FROM CinemaHallSeats
            WHERE ID IN ({','.join(['%s'] * len(seat_ids))})
        """
        result = database_execute_query_fetchall(query, seat_ids)
        return result[0]['total'] if result else 0

    

    @staticmethod
    def get_booked_seat_details(booking_id):
        query = """
        SELECT 
            chs.SeatNumber, 
            chs.SeatColumn, 
            chs.SeatType, 
            chs.SeatPrice, 
            ch.Name AS HallName,
            bs.Status
        FROM Booked_Seats bs
        INNER JOIN CinemaHallSeats chs ON bs.Seat_ID = chs.ID
        INNER JOIN CinemaHalls ch ON chs.HallID = ch.ID
        WHERE bs.BookingID = %s
        """
        params = (booking_id,)
        booked_seat_details = database_execute_query_fetchall(query, params)
        return booked_seat_details if booked_seat_details else []


    @staticmethod
    def get_all_seats() -> List[Dict[str, str]]:
        """Retrieve all seats across all halls."""
        query = "SELECT * FROM CinemaHallSeats"
        return database_execute_query_fetchall(query)
    
    @staticmethod
    def get_booked_seats_for_screening(screening_id: int) -> List[int]:
        query = "SELECT Seat_ID FROM booked_seats WHERE ScreeningID = %s"
        params = (screening_id,)
        result = database_execute_query_fetchall(query, params)
        return [row['Seat_ID'] for row in result] if result else []
    @staticmethod
    def get_booked_seat_details(booking_id):
        query = """
        SELECT 
            chs.SeatNumber, 
            chs.SeatColumn, 
            chs.SeatType, 
            chs.SeatPrice, 
            ch.Name AS HallName,
            bs.Status
        FROM booked_seats bs
        INNER JOIN cinemahallseats chs ON bs.Seat_ID = chs.ID
        INNER JOIN CinemaHalls ch ON chs.HallID = ch.ID
        WHERE bs.BookingID = %s
        """
        params = (booking_id,)
        booked_seat_details = database_execute_query_fetchall(query, params)

        # Format the results into a list of dictionaries if records are found
        if booked_seat_details:
            return [
                {
                    'seat_number': record['SeatNumber'],
                    'seat_column': record['SeatColumn'],
                    'seat_type': record['SeatType'],
                    'seat_price': record['SeatPrice'],
                    'hall_name': record['HallName'],
                    'status': record['Status']
                }
                for record in booked_seat_details
            ]
        else:
            return []



class BookingController:
    
    @staticmethod
    def get_all_bookings() -> List[model.booking.Booking]:
        query = "SELECT * FROM Bookings"
        records = database_execute_query_fetchall(query)
        return [model.booking.Booking(**record) for record in records]
    
    @staticmethod
    def get_all_bookings_with_customer_info():
        query = """
        SELECT
            b.ID AS booking_id,   
            u.ID AS user_id,        
            u.Name AS user_name,
            m.Title AS movie_title,
            s.ScreeningDate AS screening_date,
            s.StartTime AS start_time,
            s.EndTime AS end_time,
            b.Date AS booking_date,
            b.Booking_Status AS booking_status,
            h.Name AS hall_name,
            bs.ID AS seat_id,
            bs.BookingID,
            chs.SeatNumber AS seat_number,
            chs.SeatColumn AS seat_column    
        FROM
            bookings b
            JOIN users u ON b.UserID = u.ID
            JOIN movies m ON b.MovieID = m.ID
            JOIN screenings s ON b.ScreeningID = s.ID
            JOIN cinemahalls h ON s.HallID = h.ID
            JOIN booked_seats bs ON b.ID = bs.BookingID
            JOIN cinemahallseats chs ON bs.Seat_ID = chs.ID   
        ORDER BY user_name DESC, b.ID DESC;
        """
        return database_execute_query_fetchall(query)
       

    @staticmethod
    def get_bookings_by_customer_id(user_id: int):
        
        query = """
        SELECT
            b.ID AS booking_id,   
            u.ID AS user_id,        
            u.Name AS user_name,
            m.Title AS movie_title,
            s.ScreeningDate AS screening_date,
            s.StartTime AS start_time,
            s.EndTime AS end_time,
            b.Date AS booking_date,
            b.Booking_Status AS booking_status,
            h.Name AS hall_name,
            bs.ID AS seat_id,
            bs.BookingID,
            chs.SeatNumber AS seat_number,
            chs.SeatColumn AS seat_column        
        FROM
            bookings b
            JOIN users u ON b.UserID = u.ID
            JOIN movies m ON b.MovieID = m.ID
            JOIN screenings s ON b.ScreeningID = s.ID
            JOIN cinemahalls h ON s.HallID = h.ID
            JOIN booked_seats bs ON b.ID = bs.BookingID
            JOIN cinemahallseats chs ON bs.Seat_ID = chs.ID        
        WHERE
            b.UserID = %s
        ORDER BY b.ID DESC;

        """       
        params = (user_id,)     
        raw_records = database_execute_query_fetchall(query, params)
        bookings = {}
        for record in raw_records:
            booking_id = record['booking_id']
            if booking_id not in bookings:
                bookings[booking_id] = {
                    'booking_id': booking_id,
                    'booking_date':record['booking_date'],
                    'user_name': record['user_name'],
                    'movie_title': record['movie_title'],
                    'screening_date': record['screening_date'],
                    'start_time': record['start_time'],
                    'end_time': record['end_time'],
                    'hall_name': record['hall_name'],
                    'booking_date': record['booking_date'],
                    'booking_status': record['booking_status'],
                    'seats': []
                }
            bookings[booking_id]['seats'].append(f"{record['seat_column']}{record['seat_number']}")

        # convert the bookings dictionary back into a list
        return list(bookings.values())

    @staticmethod
    def get_bookings_for_hall(hall_id: int):
        query = """
        SELECT B.* FROM Bookings B
        JOIN Screenings S on B.ScreeningID = S.ID
        WHERE S.HallID=%s
        """
        params = (hall_id,)
        records = database_execute_query_fetchall(query, params)
        return [model.booking.Booking(**record) for record in records]
 
    
    @staticmethod
    def get_booking_details(booking_id):
        
        query = """
        SELECT
            b.ID AS booking_id,   
            u.ID AS user_id,        
            u.Name AS user_name,
            m.Title AS movie_title,
            s.ScreeningDate AS screening_date,
            s.StartTime AS start_time,
            s.EndTime AS end_time,
            b.Date AS booking_date,
            b.Booking_Status AS booking_status,
            h.Name AS hall_name,
            GROUP_CONCAT(DISTINCT CONCAT(chs.SeatColumn, chs.SeatNumber) ORDER BY chs.SeatColumn, chs.SeatNumber SEPARATOR ', ') AS seats
        FROM
            bookings b
            JOIN users u ON b.UserID = u.ID
            JOIN movies m ON b.MovieID = m.ID
            JOIN screenings s ON b.ScreeningID = s.ID
            JOIN cinemahalls h ON s.HallID = h.ID
            LEFT JOIN booked_seats bs ON b.ID = bs.BookingID
            LEFT JOIN cinemahallseats chs ON bs.Seat_ID = chs.ID
        WHERE b.ID = %s
        GROUP BY b.ID
        """
        try:
            # Execute the query with the booking_id as a parameter
            booking_details = database_execute_query_fetchone(query, (booking_id,))
           

            # If no details are found, return a message saying so
            if booking_details is None:
                return "No booking details found for this ID."

            # Otherwise, return the details as a dictionary, including all seats as a list
            return {
                'booking_id': booking_details['booking_id'],
                'booking_date': booking_details['booking_date'],
                'user_name': booking_details['user_name'],
                'movie_title': booking_details['movie_title'],
                'screening_date': booking_details['screening_date'],
                'screening_start_time': booking_details['start_time'],
                'screening_end_time': booking_details['end_time'],
                'hall_name': booking_details['hall_name'],
                'booking_status': booking_details['booking_status'],
                'seats': booking_details['seats'].split(', ') if booking_details['seats'] else []  # Splitting the seats if they exist
            }
        except Exception as e:
            # Return the error message for more information
            return f"An error occurred: {e}"

   
    @staticmethod
    def add_booking(booking: model.booking.Booking) -> int:
        query = """
        INSERT INTO bookings (UserID, MovieID, Date, ScreeningID,  PaymentID)
        VALUES (%s, %s, %s, %s, %s)
        """
        params = (booking.user_id, booking.movie_id, booking.date, booking.screening_id,booking.payment_id)
       
          
        booking_id = database_execute_lastrowid(query, params)
        return booking_id


    @staticmethod
    def cancel_booking(booking_id: int) -> bool:
        query = "UPDATE bookings SET Booking_Status = %s WHERE ID = %s"
        params = ('Canceled', booking_id)
        return database_execute_action(query, params)



class CouponController:
    @staticmethod
    def validate_coupon(coupon_id: int) -> bool:
        """
        Validates if the coupon is still applicable.

        Args:
        - coupon_id (int): The coupon ID to be validated.

        Returns:
        - bool: True if the coupon is valid, False otherwise.
        """
        # Fetch coupon details from the database
        query = "SELECT ExpiryDate FROM Coupons WHERE ID=%s"
        params = (coupon_id,)
        record = database_execute_query_fetchone(query, params)

        if not record:
            return False

        # Check if coupon has expired
        current_date = datetime.today().date()
        if current_date > record['ExpiryDate']:
            return False

        return True
    
    @staticmethod
    def calculate_discount(coupon_code: str, original_amount: float) -> float:
        """Get the discount for a given coupon code."""
        coupon_details = PaymentController.get_coupon_details_by_code(coupon_code)
       
        if not coupon_details:
            return 0.0  # No discount if coupon is not found

        discount_rate = float(coupon_details['Discount'])
        return (discount_rate / 100) * original_amount
    
    @staticmethod
    def apply_coupon(coupon_id: int, original_amount: float) -> tuple[float, float]:
        """
        Applies a coupon to the transaction after validation.

        Args:
        - coupon_id (int): The validated coupon ID to be applied.
        - original_amount (float): The original amount of the transaction before the discount.

        Returns:
        - Tuple[float, float]: The discount amount and the final amount after applying the discount.
        """
        # Fetch coupon's discount rate from the database
        query = "SELECT Discount FROM Coupons WHERE ID=%s"
        params = (coupon_id,)
        record = database_execute_query_fetchone(query, params)

        if not record:
            raise ValueError(f"Coupon with ID {coupon_id} not found.")

        discount_rate = record['Discount']
        discount_amount = (discount_rate / 100) * original_amount

        return discount_amount
        
