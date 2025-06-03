from flask import Blueprint, jsonify

bp = Blueprint("main", __name__)


# Define your API routes here
# Example:
# @bp.route('/')
# def index():
#     return "Hello, World!"


@bp.route("/health")
def health_check():
    return jsonify({"status": "healthy", "message": "API is running"}), 200
