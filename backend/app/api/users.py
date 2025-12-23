from flask import request, jsonify
from app.api import api
from app.models import User
from app.extensions import db
from app.models import ShoppingList
from app.serializers.shopping_list import serialize_list

@api.route("/users", methods=["GET"])
def get_users():
    users = User.query.all()
    return jsonify([
        {"id": u.id, "username": u.username, "email": u.email}
        for u in users
    ])

@api.route("/users", methods=["POST"])
def create_user():
    data = request.json

    user = User(
        username=data["username"],
        email=data["email"],
        password=data["password"],
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({"id": user.id}), 201

@api.route("/users/<int:user_id>/lists", methods=["GET"])
def get_user_lists(user_id):
    shopping_lists = ShoppingList.query.filter_by(user_id=user_id).all()
    return jsonify([serialize_list(lst) for lst in shopping_lists])