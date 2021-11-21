from config import connex_app
from flask import render_template, redirect, url_for


# Create a URL route in our application for "/"
@connex_app.route("/")
def init():
    """
    This function just responds to the browser URL
    localhost:5000/
    """
    return redirect(url_for("home"))


@connex_app.route("/home")
def home():
    return render_template("home.html", title="Welcome")
