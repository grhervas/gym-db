from flask import (render_template, redirect, url_for)
from connexion import App

# Create application instance
app = App(__name__, specification_dir="./")

# Read the swagger.yml file to configure the endpoints
app.add_api('swagger.yml')


# Create a URL route in our application for "/"
@app.route("/")
def init():
    """
    This function just responds to the browser ULR
    localhost:5000/
    """
    return redirect(url_for("home"))


@app.route("/home")
def home():
    return render_template("home.html", title="Welcome")


# If we're running in stand alone mode, run the application
if __name__ == "__main__":
    app.run(debug=True)
