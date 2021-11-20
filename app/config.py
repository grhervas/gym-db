import os

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
