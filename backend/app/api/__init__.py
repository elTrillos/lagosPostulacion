from flask import Blueprint

api = Blueprint("api", __name__)

from . import users, auth, health, products, shopping_lists
