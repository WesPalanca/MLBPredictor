from flask import Blueprint, jsonify, request
from ..models import Users
from .. import db


bp = Blueprint('user', __name__)

@bp.route('/api/users', methods=["GET"])
def getUsers():
    users = Users.query.all()
    return jsonify([user.to_dict() for user in users])


@bp.route('/api/users/register', methods=["POST"])
def registerUser():
    data = request.get_json()
    email = data.get("email")
    first_name = data.get("first_name")
    last_name = data.get("last_name")
    username = data.get("username")
    password = data.get("password")

    if Users.query.filter_by(username=username).first() or Users.query.filter_by(email = email).first():
        return jsonify({"Error":  "User already exists"}), 401
    
    new_user = Users(username= username, email= email, first_name= first_name, last_name= last_name)
    new_user.set_password(password)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "Registered User"}), 200