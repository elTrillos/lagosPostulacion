from flask import request, jsonify
from app.api import api
from app.models import User
from app.extensions import db, bcrypt

@api.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy"})
