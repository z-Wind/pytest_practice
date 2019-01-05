import pytest
from flask import g, session
import sys, os

# 若是用 pip install -e，無需下面兩行
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + "/../src")
from flaskr import create_app, db, models


@pytest.fixture
def new_User(test_client):
    user = models.User(name="Sun")

    return user


@pytest.fixture(scope="session")
def test_client():
    app = create_app("config.cfg")

    @app.before_request
    def configSetting():
        g.USERNAME = app.config["USERNAME"]
        g.PASSWORD = app.config["PASSWORD"]

    # Flask provides a way to test your application by exposing the Werkzeug test Client
    # and handling the context locals for you.
    client = app.test_client()

    # Establish an application context before running the tests.
    # for SQLAlchemy setting
    ctx = app.app_context()
    ctx.push()

    yield client  # this is where the testing happens!

    ctx.pop()


@pytest.fixture
def init_db(test_client):
    # Create the database and the database table
    db.create_all()

    yield db

    db.session.remove()
    db.drop_all()
