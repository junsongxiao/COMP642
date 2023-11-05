from flask import redirect, url_for
from app import app

"""
This module contains the route for the root page.
Note: All users can view the root, but we still use auth_handler to ensure the user is logged in
"""

@app.route("/")
def index():
    return redirect(url_for("home"))

