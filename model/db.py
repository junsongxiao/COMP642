import mysql.connector
import connect
from flask import abort


dbconn = None
connection = None

"""
This module wraps the mysql.connector library to provide a single connection to the database.
"""

def get_cursor():
    """Returns a cursor to the database, that can be used to execute queries."""
    global dbconn
    global connection
    connection = mysql.connector.connect(
        user=connect.MYSQL_USER,
        password=connect.MYSQL_PASSWORD,
        host=connect.MYSQL_HOST,
        port=connect.MYSQL_PORT,
        database=connect.MYSQL_DBNAME,
        autocommit=True
    )
    # get mysql connector to return results in a dictionary format, rather than ordered tuple
    dbconn = connection.cursor(dictionary=True)
    return dbconn

# def database_execute_action(query: str, params: tuple = None):
#     cursor = get_cursor()
#     cursor.execute(query, params)
#     connection.commit()
#     cursor.close()
#     connection.close()
def database_execute_action(query: str, params: tuple = None) -> bool:
    try:
        cursor = get_cursor()
        cursor.execute(query, params)
        affected_rows = cursor.rowcount  # Check the number of affected rows
        connection.commit()
        cursor.close()
        connection.close()
        return affected_rows > 0  # Return True if any rows were affected
    except Exception as e:
        print(f"Database execution error: {e}")
        return False

def database_execute_lastrowid(query: str, params: tuple = None):
    cursor = get_cursor()
    cursor.execute(query, params)
    connection.commit()
    last_row_id = cursor.lastrowid  # Get the last inserted row ID
    cursor.close()
    connection.close()
    return last_row_id  # Return the last inserted row ID


def database_execute_query_fetchone(query: str, params=None) -> dict:
    cursor = get_cursor()
    try:
        cursor.execute(query, params)
        result = cursor.fetchone()
        return dict(result) if result else None
    except Exception as e:
        abort(404)
        return None
    finally:
        cursor.close()
        connection.close()

def database_execute_query_fetchall(query: str, params=None) -> list:
    cursor = get_cursor()
    try:
        cursor.execute(query, params)
        results = cursor.fetchall()
        return [dict(row) for row in results]
    except Exception as e:
        print(f"An error occurred: {e}")
        return []
    finally:
        cursor.close()
        connection.close()