from flask import render_template, redirect, url_for
from app import app

"""
This module contains the routes for the error pages.
"""

@app.errorhandler(401)
def unauthorized(e):
    """Redirect to login page if the user is not logged in"""
    return redirect(url_for("login"))


@app.errorhandler(403)
def forbidden(e):
    """Render a 403 page if the user stumbles into any resources that require a higher access level"""
    return render_template("error/403.html"), 403


@app.errorhandler(404)
def page_not_found(e):
    """Render a 404 page if the user stumbles into any resources that don't exist"""
    return render_template("error/404.html"), 404
