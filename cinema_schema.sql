select * from users;
select * from movies;
select * from bookings;
select * from cinemahalls;
select * from screenings;
select * from cinemahallseats;
select * from payments;
select * from coupons;
select * from notifications;
select * from screenings;
select * from booked_seats;



-- Create cinema schema
CREATE SCHEMA IF NOT EXISTS `cinema` DEFAULT CHARACTER SET utf8;
USE `cinema`;

-- Users Table
CREATE TABLE Users (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(255),
    Address VARCHAR(255),
    Email VARCHAR(255) UNIQUE,
    Phone VARCHAR(20),
    Username VARCHAR(255) UNIQUE,
    Password VARCHAR(255),
    Type ENUM('Admin', 'FrontDeskStaff', 'Customer')
);

-- CinemaHalls Table
CREATE TABLE CinemaHalls (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(255),
    TotalSeats INT
);

-- CinemaHallSeats Table
CREATE TABLE CinemaHallSeats (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    HallID INT,
    SeatNumber INT,
    SeatColumn VARCHAR(5),
    SeatType ENUM('Regular', 'Premium'),
    SeatPrice DECIMAL(5, 2),
    Seat_Status ENUM('Available', 'Under Repair') DEFAULT 'Available',
    FOREIGN KEY (HallID) REFERENCES CinemaHalls(ID)
);

-- Movies Table
CREATE TABLE Movies (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    Title VARCHAR(255),
    Description TEXT,
    DurationMins INT,
    Language VARCHAR(50),
    ReleaseDate DATE,
    Director VARCHAR(100),
    Country VARCHAR(100),
    Genre VARCHAR(50)
);

-- Screenings Table
CREATE TABLE Screenings (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    MovieID INT,
    ScreeningDate DATE,
    StartTime TIME,
    EndTime TIME,
    HallID INT,
    FOREIGN KEY (MovieID) REFERENCES Movies(ID),
    FOREIGN KEY (HallID) REFERENCES CinemaHalls(ID)
);

-- Coupons Table
CREATE TABLE Coupons (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    ExpiryDate DATE,
    Discount DECIMAL(5, 2),
    CouponCode VARCHAR(255) NOT NULL
);

-- Payments Table
CREATE TABLE Payments (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    Amount DECIMAL(10, 2),
    CreatedOn DATE,
    CouponID INT NULL,
    Refunded INT NOT NULL DEFAULT 0,
    FOREIGN KEY (CouponID) REFERENCES Coupons(ID)
);

-- Bookings Table
CREATE TABLE Bookings (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    UserID INT,
    MovieID INT,
    Date DATE,
    ScreeningID INT,
    PaymentID INT,
    StaffID INT NULL,
    Booking_Status ENUM('Confirmed', 'Pending', 'Canceled','Refunded') DEFAULT 'Pending',
    FOREIGN KEY (UserID) REFERENCES Users(ID),
    FOREIGN KEY (MovieID) REFERENCES Movies(ID),
    FOREIGN KEY (StaffID) REFERENCES Users(ID),
    FOREIGN KEY (ScreeningID) REFERENCES Screenings(ID),
    FOREIGN KEY (PaymentID) REFERENCES Payments(ID)
);

-- Booked_Seats Table
CREATE TABLE Booked_Seats (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    ScreeningID INT,
    Seat_ID INT,
    BookingID INT,
    Status ENUM('Booked', 'Reserved') DEFAULT 'Booked',
    FOREIGN KEY (ScreeningID) REFERENCES Screenings(ID),
    FOREIGN KEY (BookingID) REFERENCES Bookings(ID),
    FOREIGN KEY (Seat_ID) REFERENCES CinemaHallSeats(ID)
);


-- Notifications Table
CREATE TABLE Notifications (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    UserID INT,
    Message TEXT,
    Date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    IsRead TINYINT DEFAULT FALSE,
    FOREIGN KEY (UserID) REFERENCES Users(ID)
);

-- USER TABLE
INSERT INTO Users (Name, Address, Email, Phone, Username, Password, Type)
VALUES
('Admin admin', '123 xxx Street, NZ', 'admin@email.com', '+11234567890', 'admin', 'admin', 'Admin'),
('staff staff', '123 xxx Street, NZ', 'staff@email.com', '+11234567891', 'staff', 'staff', 'FrontDeskStaff'),
('Customer Customer', '123 xxx Street, NZ', 'admin1@email.com', '+11234567890', 'customer', 'customer', 'Custoomer');


-- CinemaHalls Table
INSERT INTO CinemaHalls (Name, TotalSeats)
VALUES 
('Hall A', 50),
('Hall B', 50);

-- CinemaHallSeats Table for Hall 1
INSERT INTO CinemaHallSeats (HallID, SeatNumber, SeatColumn, SeatType, SeatPrice)
VALUES 
(1, 1, 'A', 'Regular', 10.00),
(1, 2, 'A', 'Premium', 15.00),
(1, 3, 'A', 'Regular', 10.00),
(1, 4, 'A', 'Premium', 15.00),
(1, 5, 'A', 'Regular', 10.00),
(1, 6, 'A', 'Premium', 15.00),
(1, 7, 'A', 'Regular', 10.00),
(1, 8, 'A', 'Premium', 15.00),
(1, 9, 'A', 'Regular', 10.00),
(1, 10, 'A', 'Premium', 15.00),

(1, 1, 'B', 'Regular', 10.00),
(1, 2, 'B', 'Premium', 15.00),
(1, 3, 'B', 'Regular', 10.00),
(1, 4, 'B', 'Premium', 15.00),
(1, 5, 'B', 'Regular', 10.00),
(1, 6, 'B', 'Premium', 15.00),
(1, 7, 'B', 'Regular', 10.00),
(1, 8, 'B', 'Premium', 15.00),
(1, 9, 'B', 'Regular', 10.00),
(1, 10, 'B', 'Premium', 15.00),

(1, 1, 'C', 'Regular', 10.00),
(1, 2, 'C', 'Premium', 15.00),
(1, 3, 'C', 'Regular', 10.00),
(1, 4, 'C', 'Premium', 15.00),
(1, 5, 'C', 'Regular', 10.00),
(1, 6, 'C', 'Premium', 15.00),
(1, 7, 'C', 'Regular', 10.00),
(1, 8, 'C', 'Premium', 15.00),
(1, 9, 'C', 'Regular', 10.00),
(1, 10, 'C', 'Premium', 15.00),

(1, 1, 'D', 'Regular', 10.00),
(1, 2, 'D', 'Premium', 15.00),
(1, 3, 'D', 'Regular', 10.00),
(1, 4, 'D', 'Premium', 15.00),
(1, 5, 'D', 'Regular', 10.00),
(1, 6, 'D', 'Premium', 15.00),
(1, 7, 'D', 'Regular', 10.00),
(1, 8, 'D', 'Premium', 15.00),
(1, 9, 'D', 'Regular', 10.00),
(1, 10, 'D', 'Premium', 15.00),

(1, 1, 'E', 'Regular', 10.00),
(1, 2, 'E', 'Premium', 15.00),
(1, 3, 'E', 'Regular', 10.00),
(1, 4, 'E', 'Premium', 15.00),
(1, 5, 'E', 'Regular', 10.00),
(1, 6, 'E', 'Premium', 15.00),
(1, 7, 'E', 'Regular', 10.00),
(1, 8, 'E', 'Premium', 15.00),
(1, 9, 'E', 'Regular', 10.00),
(1, 10, 'E', 'Premium', 15.00),

(2, 1, 'A', 'Regular', 10.00),
(2, 2, 'A', 'Premium', 15.00),
(2, 3, 'A', 'Regular', 10.00),
(2, 4, 'A', 'Premium', 15.00),
(2, 5, 'A', 'Regular', 10.00),
(2, 6, 'A', 'Premium', 15.00),
(2, 7, 'A', 'Regular', 10.00),
(2, 8, 'A', 'Premium', 15.00),
(2, 9, 'A', 'Regular', 10.00),
(2, 10, 'A', 'Premium', 15.00),

(2, 1, 'B', 'Regular', 10.00),
(2, 2, 'B', 'Premium', 15.00),
(2, 3, 'B', 'Regular', 10.00),
(2, 4, 'B', 'Premium', 15.00),
(2, 5, 'B', 'Regular', 10.00),
(2, 6, 'B', 'Premium', 15.00),
(2, 7, 'B', 'Regular', 10.00),
(2, 8, 'B', 'Premium', 15.00),
(2, 9, 'B', 'Regular', 10.00),
(2, 10, 'B', 'Premium', 15.00),


(2, 1, 'C', 'Regular', 10.00),
(2, 2, 'C', 'Premium', 15.00),
(2, 3, 'C', 'Regular', 10.00),
(2, 4, 'C', 'Premium', 15.00),
(2, 5, 'C', 'Regular', 10.00),
(2, 6, 'C', 'Premium', 15.00),
(2, 7, 'C', 'Regular', 10.00),
(2, 8, 'C', 'Premium', 15.00),
(2, 9, 'C', 'Regular', 10.00),
(2, 10, 'C', 'Premium', 15.00),

(2, 1, 'D', 'Regular', 10.00),
(2, 2, 'D', 'Premium', 15.00),
(2, 3, 'D', 'Regular', 10.00),
(2, 4, 'D', 'Premium', 15.00),
(2, 5, 'D', 'Regular', 10.00),
(2, 6, 'D', 'Premium', 15.00),
(2, 7, 'D', 'Regular', 10.00),
(2, 8, 'D', 'Premium', 15.00),
(2, 9, 'D', 'Regular', 10.00),
(2, 10, 'D', 'Premium', 15.00),


(2, 1, 'E', 'Regular', 10.00),
(2, 2, 'E', 'Premium', 15.00),
(2, 3, 'E', 'Regular', 10.00),
(2, 4, 'E', 'Premium', 15.00),
(2, 5, 'E', 'Regular', 10.00),
(2, 6, 'E', 'Premium', 15.00),
(2, 7, 'E', 'Regular', 10.00),
(2, 8, 'E', 'Premium', 15.00),
(2, 9, 'E', 'Regular', 10.00),
(2, 10, 'E', 'Premium', 15.00);

  
-- Movies Table
INSERT INTO Movies (Title, Description, DurationMins, Language, ReleaseDate, Country, Genre)
VALUES 
('Avatar', 'A paraplegic marine dispatched to the moon Pandora on a unique mission becomes torn between following his orders and protecting the world he feels is his home.', 162, 'English', '2009-12-18', 'USA', 'Sci-Fi'),
('Titanic', 'A seventeen-year-old aristocrat falls in love with a kind but poor artist aboard the luxurious, ill-fated R.M.S. Titanic.', 195, 'English', '1997-12-19', 'USA', 'Romance'),
('Interstellar', 'A group of explorers travel through a wormhole in space in an attempt to ensure humanity\'s survival.', 169, 'English', '2014-11-07', 'USA', 'Sci-Fi'),
('Inception', 'A thief who enters the dreams of others to steal secrets from their subconscious is tasked with planting an idea into the mind of a CEO.', 148, 'English', '2010-07-16', 'USA', 'Sci-Fi'),
('The Shawshank Redemption', 'Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.', 142, 'English', '1994-09-22', 'USA', 'Drama'),
('The Godfather', 'The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son.', 175, 'English', '1972-03-24', 'USA', 'Crime'),
('Pulp Fiction', 'The lives of two mob hitmen, a boxer, a gangster and his wife, and a pair of diner bandits intertwine in four tales of violence and redemption.', 154, 'English', '1994-10-14', 'USA', 'Crime'),
('The Dark Knight', 'When the menace known as the Joker emerges from his mysterious past, he wreaks havoc and chaos on the people of Gotham. The Dark Knight must accept one of the greatest psychological and physical tests of his ability to fight injustice.', 152, 'English', '2008-07-18', 'USA', 'Action'),
('The Matrix', 'A computer programmer discovers that reality as he knows it is a simulation created by machines to subjugate humanity.', 136, 'English', '1999-03-31', 'USA', 'Sci-Fi'),
('Forrest Gump', 'The presidencies of Kennedy and Johnson, the events of Vietnam, Watergate, and other historical events unfold through the perspective of an Alabama man with an IQ of 75.', 142, 'English', '1994-07-06', 'USA', 'Drama');


-- Screenings Table
INSERT INTO Screenings (MovieID, ScreeningDate, StartTime, EndTime, HallID) VALUES
(1, '2023-12-01', '18:00:00', '20:00:00', 1),
(1, '2023-12-02', '20:00:00', '22:00:00', 2),
(2, '2023-12-03', '18:00:00', '19:40:00', 1),
(2, '2023-12-04', '20:00:00', '21:40:00', 2),
(3, '2023-12-05', '18:00:00', '20:10:00', 1),
(3, '2023-12-06', '20:00:00', '22:10:00', 2),
(4, '2023-12-07', '18:00:00', '19:50:00', 1),
(4, '2023-12-08', '20:00:00', '21:50:00', 2),
(5, '2023-12-09', '18:00:00', '19:35:00', 1),
(5, '2023-12-10', '20:00:00', '21:35:00', 2);

-- Coupons Table
INSERT INTO Coupons (ExpiryDate, Discount,CouponCode) VALUES
('2023-12-31', 10.00,'CODE10'),
('2023-11-30', 5.00,'CODE05'),
('2023-10-31', 15.00,'CODE15'),
('2023-09-30', 20,'CODE20'),
('2023-08-31', 25,'CODE25');


-- payments table
INSERT INTO Payments (Amount, CreatedOn, CouponID) VALUES
(10, '2023-06-01', 1),
(15, '2023-06-01', NULL),
(10, '2023-06-02', 2),
(15, '2023-06-02', NULL),
(10, '2023-06-03', 3),
(10, '2023-06-07', NULL), 
(15, '2023-06-09', NULL),
(10, '2023-06-02', NULL),
(15, '2023-06-04', NULL),
(10, '2023-06-06', NULL);

-- booking table
INSERT INTO Bookings (UserID, MovieID, Date, ScreeningID, PaymentID, StaffID, Booking_Status) VALUES
(4, 4, '2023-06-07', 7, 6, NULL, 'Confirmed'),
(5, 5, '2023-06-09', 9, 7, 6, 'Pending'),
(6, 1, '2023-06-02', 2, 8, 7, 'Confirmed'),
(7, 2, '2023-06-04', 4, 9, 8, 'Pending'),
(8, 3, '2023-06-06', 6, 10, NULL, 'Refunded'),
(9, 4, '2023-06-08', 8, 5, 6, 'Pending'),
(10, 5, '2023-06-10', 10, 4, 7, 'Confirmed'),
(1, 2, '2023-06-03', 3, 3, 8, 'Pending'),
(2, 3, '2023-06-05', 5, 2, NULL, 'Confirmed'),
(3, 4, '2023-06-07', 7, 1, 6, 'Pending');



-- Booked Seats table

INSERT INTO Booked_Seats (ScreeningID, Seat_ID, Status, BookingID) VALUES
(1, 1, 'Booked', 1),
(1, 2, 'Reserved', 1),
(2, 3, 'Booked', 3), 
(2, 4, 'Booked', 2), 
(3, 5, 'Booked', 2),
(3, 6, 'Reserved', 2),
(4, 7, 'Booked', 4),
(4, 8, 'Booked', 3), 
(5, 9, 'Reserved', 3),
(5, 10, 'Booked', 3);


-- NOTIFICATIONS TABLE
INSERT INTO Notifications (UserID, Message) VALUES
(1, 'Your booking for "Journey to the Moon" is confirmed.'),
(2, 'Your booking for "Love in Paris" is pending.'),
(3, 'Your booking for "The Lost Jungle" is confirmed.'),
(4, 'New movie "Mystery Manor" is now available.'),
(5, 'New discount coupons are available.');

