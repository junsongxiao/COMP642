from flask import abort, session

"""A module containing functions for checking if a user is logged in and if the user is allowed to access a page"""

def is_logged_in():
    """Check if there is a session for the user"""
    if "user_id" in session and "username" in session and "role" in session:
        return True
    else:
        session.clear()
        return False

def auth_handler(role_list: list):
    """Check if the user is logged in and if the user's role is in the role list
    If not logged in, abort with 401 error and redirect to login
    If not allowed, abort with 403 error"""
   
    if is_logged_in():
        if session["role"] not in role_list:
            abort(403)
    else:
        abort(401)
    

