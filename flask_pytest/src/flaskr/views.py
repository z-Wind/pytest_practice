"""
view
"""
from flask import Blueprint

flaskr = Blueprint("finance", __name__)


@flaskr.route("/")
def index():
    return "index"
