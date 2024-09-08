from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token
from ..models import Users
from .. import db


bp = Blueprint('user', __name__)

# Get all users
@bp.route('/api/users', methods=["GET"])
def getUsers():
    users = Users.query.all()
    return jsonify([user.to_dict() for user in users])


# Register user
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


# log in user
@bp.route('/api/users/login', methods=["POST"])
def loginUser():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    # check if user exists
    user = Users.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        return jsonify({"Error": "Invalid credientials "}), 401
    
    # create jwt token
    access_token = create_access_token(identity=user.user_id)
    return jsonify({"access_token": access_token, "success": True}), 200
    
