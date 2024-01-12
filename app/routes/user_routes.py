from flask import Blueprint, jsonify
from app.models.user import User

user_bp = Blueprint('user', __name__)

@user_bp.route('/users', methods=['GET'])
def get_all_users():
    # users = User.get_all_users()
    users = ["user1", "user2", "user3", "user4"]
    return jsonify(users)

@user_bp.route('/users', methods=['POST'])
def create_user():
    # Add user creation logic here
    return jsonify(message="User created successfully!")
