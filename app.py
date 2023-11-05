
from datetime import datetime,date 
from flask import Flask, render_template, request, redirect, url_for
import model.user,model.booking,model.movie,model.cinema_hall,model.cinema_hall_seats,model.screening,model.payment,model.utilities,model.coupon
from controller.controllers import UserController, MovieController, ScreeningController, BookingController,PaymentController,CouponController,CinemaHallSeatController, CinemaHallController
from flask import session, flash

app = Flask(__name__)
app.secret_key = 'secrete_key_for_secured_sessions'





@app.route('/')
def index():
    
    return render_template('index.html')



@app.route('/dashboard')
def dashboard():
    auth = UserController.auth_handler(["Admin","Customer","FrontDeskStaff"])
    if auth:
        

        return render_template('dashboard.html')
    else:
        

        return redirect(url_for('login'))
    
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if UserController.is_logged_in():
#         return redirect(url_for('dashboard'))

#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
        

#         if UserController.login(username, password):
#             user_role = UserController.get_user_role(username)
#             user_id=UserController.get_user_id_from_username(username)
#             session['logged_in'] = True
#             session['username'] = username
#             session['Type'] = user_role
#             session['ID'] = user_id
#             print(session)
#             print("logged_in",session['logged_in'])
#             print("username",session['username'])
#             print("user_role",session['Type'])
           
#             print("user_id",session['ID'])
#             flash('Successfully logged in', 'success')
#             return redirect(url_for('dashboard'))
#         else:
#             flash('Login failed. Check your credentials.', 'danger')
            
#     return render_template('auth/login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    # If user is already logged in, redirect to dashboard
    if UserController.is_logged_in():
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Attempt to login
        if UserController.login(username, password):
            # Retrieve user role and ID for the session
            user_role = UserController.get_user_role(username)
            user_id = UserController.get_user_id_from_username(username)

            # Update the session with the new login state
            session['logged_in'] = True
            session['username'] = username
            session['Type'] = user_role
            session['ID'] = user_id

            # Flash a success message
            flash('Successfully logged in', 'success')

            # Check if there was a pre-login action
            hall_id = session.pop('pre_login_hall_id', None)
            screening_id = session.pop('pre_login_screening_id', None)
            selected_seats = session.pop('pre_login_selected_seats', None)

            # If there was a pre-login action, redirect to that
            if hall_id and screening_id:
                # You might want to repopulate the form with the selected seats here
                return redirect(url_for('display_seats', hall_id=hall_id, screening_id=screening_id))

            # Otherwise, redirect to the dashboard or other default page
            return redirect(url_for('dashboard'))
        else:
            # Flash an error message if login failed
            flash('Login failed. Check your credentials.', 'danger')

    # Show the login form
    return render_template('auth/login.html')

# @app.route('/login_to_book/<int:hall_id>/<int:screening_id>')
# def login_to_book(hall_id, screening_id):
#     # Save the hall_id and screening_id to the session
#     session['pre_login_hall_id'] = hall_id
#     session['pre_login_screening_id'] = screening_id

#     # Redirect to the login page
#     return redirect(url_for('login'))


@app.route('/logout',methods=['GET', 'POST'])
def logout():
    session.clear()
    session.pop('username', None)
    session.pop('user_role', None)
    session.pop('user_id', None)
    
    print(session)
    


    flash('Successfully logged out', 'success')
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Extracting data from the registration form
        username = request.form.get('username')
        password = request.form.get('password')
        name = request.form.get('name')
        address = request.form.get('address')
        email = request.form.get('email')
        phone = request.form.get('phone')
       

        # Check if the user can be registered
        success, message = UserController.add_user(username=username, password=password, email=email, name=name, address=address, phone=phone, user_type="Customer")

        flash(message, 'success' if success else 'danger')
        
        if success:
            return redirect(url_for('login'))

            
    return render_template('auth/register.html')


@app.route('/movies')
def movies():
    

    movies = MovieController.get_all_movies()
    

    return render_template('movies.html', movies=movies,session=session)


@app.route('/movie/<int:movie_id>/screenings')
def movie_screenings(movie_id):
    UserController.auth_handler(["Admin","Customer","FrontDeskStaff"])

    # Assuming you have a method to get a movie by its ID:
    movie = MovieController.get_movie_by_id(movie_id)
    booking = BookingController.get_booking_details(movie_id)
    today=datetime.today().date()

    if not movie:
        # Handle the error, maybe redirect to a 404 page or back to the movies page with a flash message.
        flash('Movie not found!', 'danger')
        return redirect(url_for('movies'))

    screenings = ScreeningController.get_screening_by_movie_id(movie_id)
    movie_title = movie.title
    movie_id = movie.movie_id



    return render_template('movie_screenings.html', screenings=screenings, movie_title=movie_title,movie_id=movie_id,booking=booking,today=today,session=session)




@app.route('/search_movies', methods=['GET'])
def search_movies():
    
    keywords = request.args.get('keywords', '')

    if not keywords:  # If keywords is empty or only whitespace, don't search
        movies = []  # Or set movies to None, if that's what your template expects
    else:
        movies = MovieController.search_movies_by_keywords(keywords)

   
    return render_template('index.html', movies=movies,session=session)

@app.route('/search_movies_users', methods=['GET'])
def search_movies_users():
    
    keywords = request.args.get('keywords', '')

   
    if not keywords:  
        movies = []  
    else:
        movies = MovieController.search_movies_by_keywords(keywords)

   
    return render_template('movies.html', movies=movies)


@app.route('/add_movie', methods=['GET', 'POST'])
def add_movie():
    UserController.auth_handler(["Admin","Customer","FrontDeskStaff"])
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        durationMins = int(request.form.get('durationMins'))
        language = request.form.get('language')
        releaseDate = datetime.strptime(request.form.get('releaseDate'), "%Y-%m-%d")
        country = request.form.get('country')
        genre = request.form.get('genre')


        status = MovieController.add_movie(title, description, durationMins, language, releaseDate, country, genre)

        if status:
            flash('Movie successfully added!', 'success')
            return redirect(url_for('movies'))
        else:
            flash('Unsuccessful attempt, please try again!', 'danger')

    return render_template('add_movie.html')

@app.route('/cancel_movie/<int:movie_id>', methods=['POST'])
def cancel_movie(movie_id):
    UserController.auth_handler(["Admin"])

    # Check if there are any screenings associated with the movie
    screenings = ScreeningController.get_screening_by_movie_id(movie_id)
    if screenings:
        flash('Cannot cancel movie with scheduled screenings!', 'danger')
        return redirect(url_for('movie_screenings', movie_id=movie_id))

    # If no screenings are associated, proceed to cancel the movie
    success, message = MovieController.remove_movie(movie_id)
    
    if success:
        flash('Movie successfully canceled!', 'success')
    else:
        flash(message, 'danger')
    
    return redirect(url_for('movies'))



@app.route('/screenings')
def screenings():
   
    screenings_with_movies = []
    screenings = ScreeningController.get_all_screenings()
    today=datetime.today().date()
    for screening in screenings:
        movie_id = screening['movie_id'] 
        movie = MovieController.get_movie_by_id(movie_id)
        screening['movie_title'] = movie.title if movie else 'Unknown'  
        screenings_with_movies.append(screening)  
    return render_template('screenings.html', screenings=screenings_with_movies, session=session,today=today)


@app.route('/add_screening', methods=['GET', 'POST'])
def add_screening():
    UserController.auth_handler(["Admin"])

    movies = MovieController.get_all_movies()
    halls = CinemaHallController.get_all_cinema_halls()

    if request.method == 'POST':
        movie_id = request.form.get('movie_id', '').strip()
        screeningDate = request.form.get('screeningDate', '').strip()
        start_time = request.form.get('startTime', '').strip()
        end_time = request.form.get('endTime', '').strip()
        hall_id = int(request.form.get('hall_id', '').strip())      
        hall_details = CinemaHallController.get_hall_details(hall_id)
        if not hall_details:
            flash('Hall not found.', 'danger')
            return redirect(url_for('add_screening'))

        hall_name = hall_details['name']

        try:
            screeningDate = datetime.strptime(screeningDate, "%Y-%m-%d").date()
            # Validate the screening date is not in the past
            if screeningDate < datetime.today().date():
                flash('Screening date cannot be in the past.', 'danger')
                return redirect(url_for('add_screening_for_movie', movie_id=movie_id))
            start_time = datetime.strptime(start_time, "%H:%M").time()
            end_time = datetime.strptime(end_time, "%H:%M").time()
        except ValueError:
            flash('Invalid date/time format provided.', 'danger')
            return redirect(url_for('add_screening'))

        if start_time >= end_time:
            flash('Start time must be before end time.', 'danger')
            return redirect(url_for('add_screening'))

        screening = model.screening.Screening(
            screeningDate=screeningDate,
            startTime=start_time,
            endTime=end_time,
            hall_id=hall_id,
            movie_id=movie_id,
            hall_name=hall_name
        )
        
        try:
            success = ScreeningController.add_screening(screening)
        except Exception as e:
            flash(str(e), 'danger')
            success = False

        if success:
            flash('Screening successfully added!', 'success')
            return redirect(url_for('screenings'))
        else:
            flash('Failed to add screening.', 'danger')

    return render_template('add_screening.html', movies=movies, halls=halls, movie_title=None)



@app.route('/add_screening/<int:movie_id>', methods=['GET', 'POST'])
def add_screening_for_movie(movie_id):
    UserController.auth_handler(["Admin"])
    movie = MovieController.get_movie_by_id(movie_id)
    halls = CinemaHallController.get_all_cinema_halls()

    if movie is None:
        flash('Movie not found!', 'error')
        return redirect(url_for('screenings'))  

    if request.method == 'POST':
        try:
            screeningDate = datetime.strptime(request.form.get('screeningDate'), "%Y-%m-%d").date()
            startTime = datetime.strptime(request.form.get('startTime'), "%H:%M").time()
            endTime = datetime.strptime(request.form.get('endTime'), "%H:%M").time()
            hall_id = int(request.form.get('hall_id'))
            # Validate the screening date is not in the past
            if screeningDate < datetime.today().date():
                flash('Screening date cannot be in the past.', 'danger')
                return redirect(url_for('add_screening_for_movie', movie_id=movie_id))

            # Fetch hall details including the name
            hall_details = CinemaHallController.get_hall_details(hall_id)
            if not hall_details:
                flash('Hall not found.', 'danger')
                return redirect(url_for('add_screening_for_movie', movie_id=movie_id))

            # Use the hall name from the details
            hall_name = hall_details['name']
            
            # Create a Screening object
            screening = model.screening.Screening(
                screeningDate=screeningDate,
                startTime=startTime,
                endTime=endTime,
                hall_id=hall_id,
                movie_id=movie_id,
                hall_name=hall_name
            )

            # Add the screening using the ScreeningController
            status = ScreeningController.add_screening(screening)

            if status:
                flash('Screening successfully added!', 'success')
                return redirect(url_for('screenings'))
            else:
                flash('Failed attempt for adding screening', 'danger')
        except ValueError as e:
            flash(f'Error processing form data: {e}', 'danger')
        except Exception as e:
            flash(f'Unexpected error: {e}', 'danger')

    return render_template('add_screening.html', movie=movie, movie_title=movie.title, halls=halls, movie_id=movie_id)

# @app.route('/delete_screening/<int:screening_id>', methods=['POST'])
# def delete_screening(screening_id):
#     UserController.auth_handler(["Admin"])
#     success, message = ScreeningController.remove_screening(screening_id)
    
#     if success:
#         flash('Screening successfully deleted!', 'success')
#     else:
#         flash(message, 'danger')
    
#     return redirect(url_for('screenings'))
@app.route('/delete_screening/<int:screening_id>', methods=['POST'])
def delete_screening(screening_id):
    UserController.auth_handler(["Admin"])
    success, message = ScreeningController.remove_screening(screening_id)
    
    if success:
        flash('Screening successfully deleted!', 'success')
    else:
        flash(message, 'danger')
    
    return redirect(url_for('screenings'))



@app.route('/display_seats/<int:hall_id>/<int:screening_id>', methods=['GET'])
def display_seats(hall_id, screening_id):
    
    booked_seats = CinemaHallSeatController.get_booked_seats_for_screening(screening_id)
    
    
    screening_details = ScreeningController.get_screening_details(screening_id)
    
   
    all_seats = CinemaHallSeatController.get_all_seats_for_hall(hall_id)
    
   
    hall_details = CinemaHallController.get_hall_details(hall_id)
    
    return render_template('seats.html', 
                       booked_seats=booked_seats, 
                       screening=screening_details, 
                       all_seats=all_seats, 
                       hall=hall_details,
                       hall_id=hall_id,
                       screening_id=screening_id)



@app.route('/calculate_total_price/<int:hall_id>/<int:screening_id>', methods=['POST'])
def calculate_total_price(hall_id, screening_id):
    selected_seats = request.form.getlist('selected_seats')
    
    
    total_price = CinemaHallSeatController.get_booked_seats_total_price(selected_seats)
    
   
    screenings = ScreeningController.get_screenings_by_hall(hall_id)
    booked_seats = CinemaHallSeatController.get_booked_seats_for_screening(screening_id)
    available_seats = CinemaHallSeatController.get_available_seats_for_hall(hall_id)
    screening=ScreeningController.get_screening_details(screening_id)
    
   
    return render_template('seats.html', selected_seats=selected_seats,total_price=total_price, hall_id=hall_id,screening_id=screening_id,screening=screening,screenings=screenings, booked_seats=booked_seats, available_seats=available_seats)


@app.route('/booking_details/<int:booking_id>', methods=['GET'])
def booking_details(booking_id):
    booking = BookingController.get_booking_details(booking_id)

    # Check if booking details were found
    if booking is None:
        flash('Booking details not found!', 'error')
        return redirect(url_for('index')) 
    
    return render_template('booking_details.html', booking=booking)        

@app.route('/my_bookings')
def my_bookings():
    UserController.auth_handler(["Admin","Customer","FrontDeskStaff"])
    
    user_id = session.get('ID')
    
    if not user_id:
        flash("Please log in to view your bookings.", "danger")
        return redirect(url_for('login')) 

    bookings = BookingController.get_bookings_by_customer_id(user_id)
    today=datetime.today().date()
    total_price = {}
    for booking in bookings:       
        booking['start_time'] = str((datetime.min + booking['start_time']).time())[:5]
        booking['end_time'] = str((datetime.min + booking['end_time']).time())[:5]
        booking_id = booking['booking_id']
        price = PaymentController.get_total_due(booking_id)
        
        # Add the total_price to the corresponding booking's sum in the dictionary
        if booking_id in total_price:
            total_price[booking_id] += price
        else:
            total_price[booking_id] = price
    
    return render_template('my_bookings.html', bookings=bookings, today=today, total_price=total_price)


@app.route('/view_bookings')
def view_bookings():
    UserController.auth_handler(["Admin","FrontDeskStaff"])    
    bookings = BookingController.get_all_bookings_with_customer_info()    
    today=datetime.today().date()
    total_price = {}
    for booking in bookings:       
        booking['start_time'] = str((datetime.min + booking['start_time']).time())[:5]
        booking['end_time'] = str((datetime.min + booking['end_time']).time())[:5]
        booking_id = booking['booking_id']
        price = PaymentController.get_total_due(booking_id)
        
        # Add the total_price to the corresponding booking's sum in the dictionary
        if booking_id in total_price:
            total_price[booking_id] += price
        else:
            total_price[booking_id] = price
    
    return render_template('view_bookings.html', bookings=bookings, today=today, total_price=total_price)


@app.route('/booking_payment/<int:booking_id>', methods=['GET'])
def booking_payment(booking_id): 
    booking = BookingController.get_booking_details(booking_id)
   
    total_price = PaymentController.get_total_due(booking_id)
   
    return render_template('payment.html', booking=booking,  booking_id=booking_id, total_price=total_price, session=session)
    
    
@app.route('/apply_coupon/<int:booking_id>', methods=['POST'])
def apply_coupon(booking_id):
    try:
        coupon_code = request.form.get('coupon')
        if not coupon_code:
            flash('No coupon code entered.', 'info')
            return redirect(url_for('booking_payment', booking_id=booking_id))

        original_amount = float(PaymentController.get_total_due(booking_id))
        coupon_details = PaymentController.get_coupon_details_by_code(coupon_code)

        if coupon_details and CouponController.validate_coupon(coupon_details['ID']):
            discount_amount = float(CouponController.calculate_discount(coupon_details['CouponCode'], original_amount))
            amount_to_pay = original_amount - discount_amount
            session['amount_to_pay'] = amount_to_pay  # Store in session
            session['coupon_id'] = coupon_details['ID']  # Store coupon ID in session
            flash(f'Coupon {coupon_code} has been applied. You will be saving ${discount_amount:.2f}!', 'success')
        else:
            flash('Invalid or expired coupon code!', 'error')
            session['amount_to_pay'] = original_amount  # No discount, store original amount

    except Exception as e:
        flash(f'An error occurred while applying the coupon: {e}', 'error')
        # In case of exception, revert to original amount
        session['amount_to_pay'] = original_amount

    return redirect(url_for('booking_payment', booking_id=booking_id))


@app.route('/make_payment/<int:booking_id>', methods=['POST'])
def make_payment(booking_id):
    
    
    # Retrieve the amount to pay from the session or calculate it again
    amount_to_pay = float(session.get('amount_to_pay', PaymentController.get_total_due(booking_id)))
   

    entered_amount = float(request.form.get('amount', 0))
    

    if entered_amount < amount_to_pay:
        flash('Entered amount is less than the amount to pay. Please try again.', 'error')
        
    elif entered_amount > amount_to_pay:
        flash('Entered amount is greater than the amount to pay. Please try again.', 'error')

    # Make the payment
    payment_id = PaymentController.make_payment(amount_to_pay, session.get('coupon_id'))
    
    user_id = session.get('user_id')
    if payment_id:
        # Update the payment and booking status
        if PaymentController.update_payment_and_status_for_booking(booking_id, payment_id, 'Confirmed'):
            flash('Payment successful and booking confirmed!', 'success')
            session.pop('amount_to_pay', None)
            session.pop('coupon_id', None)
            return redirect(url_for('my_bookings',ID=user_id))
        else:
            flash('Booking could not be updated. Please contact support.', 'error')
    else:
        flash('Payment failed. Please try again.', 'error')
    
    return redirect(url_for('booking_payment', booking_id=booking_id))

# @app.route('/make_booking/<int:hall_id>/<int:screening_id>', methods=['GET', 'POST'])
# def make_booking(hall_id, screening_id):
#     # Check if the user is logged in
#     if not UserController.is_logged_in():
#         # Redirect to the login page with a message
#         flash('Please log in to continue with the booking.', 'info')
#         return redirect(url_for('login'))

    
#     booking_user_id = session.get('user_id')

#     if request.method == 'POST':
#         UserController.auth_handler(["Admin", "Customer", "FrontDeskStaff"])

#         # Check if the booking is being made by FrontDeskStaff
#         if session.get('Type') == 'FrontDeskStaff':
#             # Get customer details from form
#             name = request.form.get('name')
#             username = request.form.get('username')  
#             password = request.form.get('password')
#             email = request.form.get('email')  
#             phone = request.form.get('phone')
#             address = request.form.get('address')              
#             customer_user_id = UserController.add_user(name,username, password,email,phone,address,"Customer")
#         else:
#             # If not FrontDeskStaff, the booking user is the logged in user
#             customer_user_id = booking_user_id

#         # Create the booking
#         selected_seats = request.form.getlist('selected_seats')
#         movie_id = request.form.get('movie_id')
#         booking_date = datetime.today()
#         booking = model.booking.Booking(
#             user_id=customer_user_id,
#             screening_id=screening_id,
#             movie_id=movie_id,
#             payment_id=None,
#             date=booking_date
#         )
#         booking_id = BookingController.add_booking(booking)
#         booking.booking_id = booking_id

#         CinemaHallSeatController.book_seat(screening_id, selected_seats, booking_id)

#         # Redirect to payment page after booking
#         return redirect(url_for('booking_payment', booking_id=booking_id))

#     # For GET requests, just show the seat selection form
#     # You need to fetch the seats and booked seats again for rendering the form
 
#     all_seats = CinemaHallSeatController.get_all_seats_for_hall(hall_id)
    
#     booked_seats = CinemaHallSeatController.get_booked_seats_for_screening(screening_id)

#     return render_template('seats.html', all_seats=all_seats, booked_seats=booked_seats, hall_id=hall_id, screening_id=screening_id)




@app.route('/make_booking/<int:hall_id>/<int:screening_id>', methods=['GET', 'POST'])
def make_booking(hall_id, screening_id):
    # Check if the user is logged in
    if not UserController.is_logged_in():
        # Redirect to the login page with a message
        flash('Please log in to continue with the booking.', 'info')
        return redirect(url_for('login'))

    if request.method == 'POST':
        UserController.auth_handler(["Admin", "Customer", "FrontDeskStaff"])
        print(session)

        # Check if the booking is being made by FrontDeskStaff
        if session.get('type') == 'FrontDeskStaff':
            # Get customer details from form
            name = request.form.get('name')
            username = request.form.get('username')  
            password = request.form.get('password')
            email = request.form.get('email')  
            phone = request.form.get('phone')
            address = request.form.get('address')
            print("name",name)
            print("username",username)

            # Check if the email or username already exists
            if UserController.get_user_id_from_username(username):
                print("username already exist")
                flash('Username or Email already exists.', 'danger')
                return redirect(request.url)  # Stay on the same page

            # Attempt to create a new user
            success, message_or_user_id = UserController.add_user(name, address, email, phone, username, password, "Customer")
            print("success",success)
            # If user creation was not successful, show an error message
            if not success:
                flash(message_or_user_id, 'danger')
                print(request.url)
                return redirect(request.url)  # Stay on the same page

            # If successful, set the customer_user_id to the new user's ID
            customer_user_id = message_or_user_id
            print("customer_user_id",customer_user_id)
        else:
            # If not FrontDeskStaff, the booking user is the logged in user
            customer_user_id = session.get('user_id')
            print("customer_user_id",customer_user_id)

        # Create the booking
        selected_seats = request.form.getlist('selected_seats')
        print("selected_seats",selected_seats)
        movie_id = request.form.get('movie_id')
        booking_date = datetime.today()
        booking = model.booking.Booking(
            user_id=customer_user_id,
            screening_id=screening_id,
            movie_id=movie_id,
            payment_id=None,
            date=booking_date
        )
        
        # Attempt to add the booking
        try:
            booking_id = BookingController.add_booking(booking)

        except Exception as e:
            flash(str(e), 'danger')
            return redirect(request.url)  # Stay on the same page
        
        CinemaHallSeatController.book_seat(screening_id, selected_seats, booking_id)

        # Redirect to payment page after booking
        return redirect(url_for('booking_payment', booking_id=booking_id))
    elif request.method == 'GET':

        # For GET requests, just show the seat selection form
        screening = ScreeningController.get_screening_by_id(screening_id)
        print("make booking route",screening)
        if screening:
                movie_id = screening['movie_id'] 
        else:
            flash('Screening not found.', 'danger')
            return redirect(url_for('movies'))
        all_seats = CinemaHallSeatController.get_all_seats_for_hall(hall_id)
        print("all seats",all_seats)
        booked_seats = CinemaHallSeatController.get_booked_seats_for_screening(screening_id)
        print("booked seats",booked_seats)
    

        return render_template('seats.html', all_seats=all_seats, booked_seats=booked_seats, hall_id=hall_id, screening_id=screening_id,screening=screening)

# @app.route('/make_booking/<int:hall_id>/<int:screening_id>', methods=['POST'])
# def make_booking(hall_id, screening_id):
    
#     # Check if the user is logged in
#     if not UserController.is_logged_in():
#         # Save the hall_id and screening_id to the session to preserve state
#         session['pre_login_hall_id'] = hall_id
#         session['pre_login_screening_id'] = screening_id
#         session['pre_login_selected_seats'] = request.form.getlist('selected_seats')
#         flash('Please log in to continue with the booking.', 'info')
        
#         # Redirect to the login page
#         return redirect(url_for('login'))
    
#     UserController.auth_handler(["Admin","Customer","FrontDeskStaff"])
#     # If the user is logged in, proceed with the booking process
#     selected_seats = session.pop('pre_login_selected_seats', request.form.getlist('selected_seats'))
    
    
#     # selected_seats = request.form.getlist('selected_seats')
 
   
#     movie_id = request.form['movie_id']
#     user_id = session.get('user_id')  
    
   
#     booking_date = datetime.today()
#     booking = model.booking.Booking(
        
#         user_id=user_id,
#         screening_id=screening_id,
#         movie_id=movie_id,
#         payment_id=None,
#         date=booking_date
#     )
#     booking_id = BookingController.add_booking(booking)
   
#     booking.booking_id=booking_id
   
#     CinemaHallSeatController.book_seat(screening_id, selected_seats,booking_id)
#     # Redirect to payment page after booking
#     return redirect(url_for('booking_payment', booking_id=booking_id))

@app.route('/cancel_booking/<int:booking_id>', methods=['GET','POST'])
def cancel_booking(booking_id):

    UserController.auth_handler(["Admin","Customer","FrontDeskStaff"])

    # Check if the booking exists and can be canceled
    booking = BookingController.get_booking_details(booking_id)
    if booking is None:
        flash('Booking not found!', 'error')
        if session.get('Type') == 'Customer':
            return redirect(url_for('my_bookings'))
        else:
            return redirect(url_for('view_bookings'))

    # Perform the cancellation
    try:
        result = BookingController.cancel_booking(booking_id)
        if result:
            flash('Booking successfully canceled!', 'success')
        else:
            flash('Cancellation failed!', 'error')
    except Exception as e:
        flash(f'An error occurred while canceling the booking: {e}', 'error')

    
    if session.get('Type') == 'Customer':
        return redirect(url_for('my_bookings'))
    else:
        return redirect(url_for('view_bookings'))

@app.route('/refund_booking/<int:booking_id>', methods=['GET', 'POST'])
def refund_booking(booking_id):
    UserController.auth_handler(["Admin","Customer","FrontDeskStaff"])
    

    # Check if the booking exists and can be refunded
    booking = BookingController.get_booking_details(booking_id)
    if booking is None:
        flash('Booking not found!', 'error')
        if session.get('Type') == 'Customer':
            return redirect(url_for('my_bookings'))
        else:
            return redirect(url_for('view_bookings'))
        
    payment_id=PaymentController.get_payment_id(booking_id)
    

    
    # Perform the refund
    try:
        refund=PaymentController.refund_payment(payment_id)
        if refund:
            flash('Booking successfully refunded!', 'success')
        else:
            flash('Refund failed!', 'error')
    except Exception as e:
        flash(f'An error occurred while refunding the booking: {e}', 'error')
    
    if session.get('Type') == 'Customer':
        return redirect(url_for('my_bookings'))
    else:
        return redirect(url_for('view_bookings'))


if __name__ == "__main__":
    app.debug = True
    app.run()