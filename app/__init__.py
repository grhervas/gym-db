from connexion import App
from config import Config, base_dir
from flask import (render_template, redirect, url_for)
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow


# Create the Connexion application instance
connex_app = App(__name__, specification_dir=base_dir)

# Read the swagger.yml file to configure endpoints
connex_app.add_api("swagger.yml")

# Get the underlying Flask app instance and configure it
app = connex_app.app
app.config.from_object(Config)

# Create the SQLAlchemy db instance
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Initialize Marshmallow
ma = Marshmallow(app)


# Create a URL route in our application for "/"
@connex_app.route("/")
def init():
    """
    This function just responds to the browser ULR
    localhost:5000/
    """
    return redirect(url_for("home"))


@connex_app.route("/home")
def home():
    return render_template("home.html", title="Welcome")


# If we're running in stand alone mode, run the application
if __name__ == "__main__":
    connex_app.run(debug=True)
