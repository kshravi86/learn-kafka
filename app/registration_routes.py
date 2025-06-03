from datetime import datetime

from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from .models import Registration, User, db

reg_bp = Blueprint("registrations", __name__, url_prefix="/registrations")


@reg_bp.route("", methods=["POST"])
@jwt_required()
def create_registration():
    data = request.get_json()
    sport = data.get("sport")
    training_level = data.get("training_level")
    current_user_id = get_jwt_identity()

    if not sport or not training_level:
        return jsonify({"message": "Missing sport or training_level"}), 400

    user = User.query.get(current_user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    new_registration = Registration(
        user_id=current_user_id,
        sport=sport,
        training_level=training_level,
        registration_date=datetime.utcnow(),
    )
    db.session.add(new_registration)
    db.session.commit()

    return (
        jsonify(
            {
                "message": "Registration successful",
                "registration": new_registration.to_dict(),
            }
        ),
        201,
    )


@reg_bp.route("", methods=["GET"])
@jwt_required()
def get_registrations():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    registrations = Registration.query.filter_by(user_id=current_user_id).all()
    return jsonify([reg.to_dict() for reg in registrations]), 200
