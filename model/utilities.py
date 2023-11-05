import datetime

def validate_datetime(dt_str):
    try:
        # Parse the input string to a datetime object
        dt = datetime.datetime.strptime(dt_str, '%Y-%m-%d %H:%M:%S')

        # Check if the minutes are divisible by 15 (quarter-hourly)
        if dt.minute % 15 != 0:
            raise ValueError("Date/time must be on a quarter-hourly interval.")

        # If everything is fine, return the validated datetime object
        return dt

    except ValueError as e:
        # Handle the validation error
        raise ValueError("You can only book for quarter-hourly intervals. Please enter a valid time.")