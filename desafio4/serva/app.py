from flask import Flask, jsonify, request
from datetime import datetime, timedelta

app = Flask(__name__)

USERS = [
    {
        "id": 1,
        "name": "Alice Silva",
        "email": "alice@email.com",
        "active": True,
        "registration_date": (datetime.now() - timedelta(days=365)).isoformat(),
        "profile": "administrator"
    },
    {
        "id": 2,
        "name": "Bob Santos",
        "email": "bob@email.com",
        "active": True,
        "registration_date": (datetime.now() - timedelta(days=180)).isoformat(),
        "profile": "editor"
    },
    {
        "id": 3,
        "name": "Carol Oliveira",
        "email": "carol@email.com",
        "active": False,
        "registration_date": (datetime.now() - timedelta(days=90)).isoformat(),
        "profile": "reader"
    },
    {
        "id": 4,
        "name": "David Costa",
        "email": "david@email.com",
        "active": True,
        "registration_date": (datetime.now() - timedelta(days=30)).isoformat(),
        "profile": "editor"
    },
    {
        "id": 5,
        "name": "Eva Martins",
        "email": "eva@email.com",
        "active": True,
        "registration_date": (datetime.now() - timedelta(days=7)).isoformat(),
        "profile": "reader"
    }
]


@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        "status": "healthy",
        "service": "Service A - User Management",
        "timestamp": datetime.now().isoformat()
    }), 200


@app.route('/api/users', methods=['GET'])
def list_users():
    try:
        users = USERS.copy()

        active_param = request.args.get('active')
        if active_param:
            active_bool = active_param.lower() == 'true'
            users = [user for user in users if user['active'] == active_bool]

        profile_param = request.args.get('profile')
        if profile_param:
            users = [user for user in users if user['profile'] == profile_param]

        return jsonify({
            "total": len(users),
            "users": users,
            "timestamp": datetime.now().isoformat()
        }), 200
    except Exception as error:
        return jsonify({"error": str(error)}), 500


@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    try:
        user = next((user for user in USERS if user['id'] == user_id), None)
        if not user:
            return jsonify({"error": f"User {user_id} not found"}), 404

        return jsonify({
            "user": user,
            "timestamp": datetime.now().isoformat()
        }), 200
    except Exception as error:
        return jsonify({"error": str(error)}), 500


@app.route('/api/users', methods=['POST'])
def create_user():
    try:
        data = request.get_json()

        if not data.get('name') or not data.get('email'):
            return jsonify({"error": "Name and email are required"}), 400

        new_id = max(user['id'] for user in USERS) + 1
        new_user = {
            "id": new_id,
            "name": data.get('name'),
            "email": data.get('email'),
            "active": data.get('active', True),
            "registration_date": datetime.now().isoformat(),
            "profile": data.get('profile', 'reader')
        }

        USERS.append(new_user)

        return jsonify({
            "message": "User created successfully",
            "user": new_user,
            "timestamp": datetime.now().isoformat()
        }), 201
    except Exception as error:
        return jsonify({"error": str(error)}), 500


@app.route('/api/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    try:
        user = next((user for user in USERS if user['id'] == user_id), None)
        if not user:
            return jsonify({"error": f"User {user_id} not found"}), 404

        data = request.get_json()

        if 'name' in data:
            user['name'] = data['name']
        if 'email' in data:
            user['email'] = data['email']
        if 'active' in data:
            user['active'] = data['active']
        if 'profile' in data:
            user['profile'] = data['profile']

        return jsonify({
            "message": "User updated successfully",
            "user": user,
            "timestamp": datetime.now().isoformat()
        }), 200
    except Exception as error:
        return jsonify({"error": str(error)}), 500


@app.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        user = next((user for user in USERS if user['id'] == user_id), None)
        if not user:
            return jsonify({"error": f"User {user_id} not found"}), 404

        USERS.remove(user)

        return jsonify({
            "message": f"User {user_id} deleted successfully",
            "timestamp": datetime.now().isoformat()
        }), 200
    except Exception as error:
        return jsonify({"error": str(error)}), 500


@app.route('/api/users/statistics/summary', methods=['GET'])
def statistics():
    total = len(USERS)
    active_users = len([user for user in USERS if user['active']])
    inactive_users = total - active_users

    profiles = {}
    for user in USERS:
        profile = user['profile']
        profiles[profile] = profiles.get(profile, 0) + 1

    return jsonify({
        "total_users": total,
        "active": active_users,
        "inactive": inactive_users,
        "by_profile": profiles,
        "timestamp": datetime.now().isoformat()
    }), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=False)