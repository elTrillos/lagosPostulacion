from flask import request, jsonify
from app.api import api
from app.models import User
from app.extensions import db, bcrypt

@api.route("/auth/login", methods=["POST"])
def login():
    data = request.json

    user = User.query.filter_by(email=data["email"]).first()

    if not user or not user.check_password(data["password"]):
        return {"error": "Invalid credentials"}, 401

    #login_user(user)

    return {"message": "Logged in"}

@api.route("/auth/register", methods=["POST"])
def register():
    data = request.json

    if User.query.filter_by(email=data["email"]).first():
        return {"error": "User already exists"}, 400

    user = User(email=data["email"])
    user.set_password(data["password"])

    db.session.add(user)
    db.session.commit()

    return {"message": "User created"}, 201