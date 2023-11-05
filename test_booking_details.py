# test_booking_details.py
import pytest
from controller.controllers import BookingController, CinemaHallSeatController

# Mocked database execute function which will be used to replace the real one
def mock_database_execute_query_fetchone(query, params):
    # This is where you define what you want to return for your tests
    if params[0] == 47:  # Assuming 47 is a valid booking_id for your test
        return {
            'ID': 47,
            'Name': 'John Doe',
            'Title': 'Some Movie',
            'StartTime': '18:00:00',
            'HallName': 'Main Hall',
            'Date': '2023-01-01',
            'PaymentID': 1
        }
    else:
        return None

def mock_database_execute_query_fetchall(query, params):
    # This is where you define what you want to return for your tests
    if params[0] == 47:  # Assuming 47 is a valid booking_id for your test
        return [
            {'SeatNumber': 1, 'SeatColumn': 'A', 'SeatType': 'Regular', 'SeatPrice': 10.0, 'HallName': 'Main Hall', 'Status': 'Booked'}
            # Add more dictionaries if needed to represent multiple seats
        ]
    else:
        return []

# Test for get_booking_details
def test_get_booking_details(mocker):
    mocker.patch('yourapplication.some_module.database_execute_query_fetchone', side_effect=mock_database_execute_query_fetchone)

    booking_details = BookingController.get_booking_details(47)
    assert booking_details is not None
    assert booking_details['booking_id'] == 47
    # Add more asserts to validate all the fields

# Test for get_booked_seat_details
def test_get_booked_seat_details(mocker):
    mocker.patch('yourapplication.some_module.database_execute_query_fetchall', side_effect=mock_database_execute_query_fetchall)

    seat_details = CinemaHallSeatController.get_booked_seat_details(47)
    assert seat_details is not None
    assert len(seat_details) > 0  # Assuming there
