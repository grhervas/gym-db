import os
from connexion import App
from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate
from flask_marshmallow import Marshmallow

base_dir = os.path.abspath(os.path.dirname(__file__))
sqlite_url = "sqlite:///" + os.path.join(base_dir, "gym.db")


class Config(object):
    SECRET_KEY = (os.environ.get("SECRET_KEY")
                  or
                  os.urandom(32))
    # Configure the SQLAlchemy part of the app instance
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = (os.environ.get("DATABASE_URL")
                               or
                               sqlite_url)
    SQLALCHEMY_TRACK_MODIFICATIONS = False


# Create the Connexion application instance
connex_app = App(__name__, specification_dir=base_dir)

# Get the underlying Flask app instance and configure it
app = connex_app.app
app.config.from_object(Config)

# Create the SQLAlchemy db instance
db = SQLAlchemy(app)
# migrate = Migrate(app, db)

# Initialize Marshmallow
ma = Marshmallow(app)
