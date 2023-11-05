from flask import render_template, request, redirect, url_for, session, flash
from app import app
import controller.controllers

from routes.session_utils import is_logged_in

"""
This module contains the routes for the login, registration and logout pages.
"""

@app.route("/login", methods=["GET", "POST"])
def login():
    # Redirect to index if the user is already logged in
    if is_logged_in():
        return redirect(url_for("index"))

    # If the request method is POST, attempt to log the user in
    if request.method == "POST":
        if controller.controllers.UserController.login(request.form.get("username"), request.form.get("password")):
            
            return redirect(url_for("dashboard"))
        else:
            error_msg = "Invalid username or password. Please try again."
            return render_template("auth/login.html", error_msg=error_msg)
    # If the request method is GET, display the login form
    else:
        return render_template("login.html")


@app.route("/logout", methods=["GET", "POST"])
def logout():
    """Logs the user out"""
    if is_logged_in():
        session.clear()
    return redirect(url_for("index"))
