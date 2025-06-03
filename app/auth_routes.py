from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token
from flask_login import login_required, login_user, logout_user

from .models import User, db

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/register_user", methods=["POST"])
def register_user():
    data = request.get_json()
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not username or not email or not password:
        return jsonify({"message": "Missing username, email, or password"}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"message": "Username already exists"}), 409
    if User.query.filter_by(email=email).first():
        return jsonify({"message": "Email already exists"}), 409

    new_user = User(username=username, email=email)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"message": "Missing email or password"}), 400

    user = User.query.filter_by(email=email).first()

    if user and user.check_password(password):
        login_user(user)  # Flask-Login session still managed
        access_token = create_access_token(identity=user.id)
        return (
            jsonify({"message": "Login successful", "access_token": access_token}),
            200,
        )

    return jsonify({"message": "Invalid email or password"}), 401


@auth_bp.route("/logout", methods=["POST"])
def logout():
    return (
        jsonify(
            {
                "message": "Logout successful. Please discard your JWT token on the client-side."
            }
        ),
        200,
    )
