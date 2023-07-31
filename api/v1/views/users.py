#!usr/bin/python3
"""users"""

from flask import jsonify, request, abort
from models import storage
from models.user import User
from api.v1.views import app_views


@app_views.route('/users', methods=['GET'])
def get_users():
    users = storage.all(User)
    user_list = [user.to_dict() for user in users.values()]
    return jsonify(user_list)


@app_views.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400
    if 'email' not in data:
        return jsonify({"error": "Missing email"}), 400
    if 'password' not in data:
        return jsonify({"error": "Missing password"}), 400
    new_user = User(**data)
    new_user.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    user = storage.get(User, user_id)
    if not user:
        abort(404)

    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400

    ignore_keys = ['id', 'email', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(user, key, value)

    user.save()
    return jsonify(user.to_dict()), 200

