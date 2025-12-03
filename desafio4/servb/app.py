from flask import Flask, jsonify
import requests
from datetime import datetime
import time

app = Flask(__name__)

SERVICE_A_URL = "http://service-a:5001"

def get_users_service_a():
    try:
        response = requests.get(f"{SERVICE_A_URL}/api/users", timeout=5)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except Exception as error:
        print(f"Error connecting to Service A: {error}")
        return None

def get_user_service_a(user_id):
    try:
        response = requests.get(f"{SERVICE_A_URL}/api/users/{user_id}", timeout=5)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except Exception as error:
        print(f"Error connecting to Service A: {error}")
        return None

def get_statistics_service_a():
    try:
        response = requests.get(f"{SERVICE_A_URL}/api/users/statistics/summary", timeout=5)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except Exception as error:
        print(f"Error connecting to Service A: {error}")
        return None

@app.route('/health', methods=['GET'])
def health():
    try:
        response = requests.get(f"{SERVICE_A_URL}/health", timeout=2)
        service_a_status = "available" if response.status_code == 200 else "unavailable"
    except Exception:
        service_a_status = "unavailable"

    return jsonify({
        "status": "healthy",
        "service": "Service B - Analysis and Visualization",
        "service_a": service_a_status,
        "timestamp": datetime.now().isoformat()
    }), 200

@app.route('/api/users/formatted', methods=['GET'])
def users_formatted():
    try:
        data = get_users_service_a()

        if not data:
            return jsonify({
                "error": "Could not connect to Service A",
                "service_a_url": SERVICE_A_URL
            }), 503

        users = data.get('users', [])

        formatted_users = []
        for user in users:
            registration_date = datetime.fromisoformat(user['registration_date'])
            days_since_registration = (datetime.now() - registration_date).days

            formatted_users.append({
                "id": user['id'],
                "name": user['name'],
                "email": user['email'],
                "status": "Active" if user['active'] else "Inactive",
                "profile": user['profile'].capitalize(),
                "registration": f"{days_since_registration} days ago" if days_since_registration > 0 else "Today",
                "complete_date": user['registration_date']
            })

        return jsonify({
            "total": len(formatted_users),
            "users": formatted_users,
            "source": "Service A",
            "timestamp": datetime.now().isoformat()
        }), 200
    except Exception as error:
        return jsonify({"error": str(error)}), 500

@app.route('/api/users/report', methods=['GET'])
def users_report():
    try:
        user_data = get_users_service_a()
        stats_data = get_statistics_service_a()

        if not user_data or not stats_data:
            return jsonify({
                "error": "Could not connect to Service A"
            }), 503

        users = user_data.get('users', [])
        stats = stats_data

        active_users = [user for user in users if user['active']]
        inactive_users = [user for user in users if not user['active']]

        active_formatted = []
        for user in active_users:
            registration_date = datetime.fromisoformat(user['registration_date'])
            days = (datetime.now() - registration_date).days
            active_formatted.append({
                "name": user['name'],
                "email": user['email'],
                "profile": user['profile'].upper(),
                "active_for_days": days
            })

        inactive_formatted = []
        for user in inactive_users:
            inactive_formatted.append({
                "name": user['name'],
                "email": user['email'],
                "profile": user['profile'].upper()
            })

        report = {
            "title": "User Report",
            "summary": {
                "total_users": stats['total_users'],
                "active_users": stats['active'],
                "inactive_users": stats['inactive'],
                "active_percentage": round((stats['active'] / stats['total_users'] * 100), 2) if stats['total_users'] > 0 else 0
            },
            "profile_distribution": stats['by_profile'],
            "active_users": active_formatted,
            "inactive_users": inactive_formatted,
            "source": "Consumed from Service A",
            "timestamp": datetime.now().isoformat()
        }

        return jsonify(report), 200
    except Exception as error:
        return jsonify({"error": str(error)}), 500

@app.route('/api/users/<int:user_id>/details', methods=['GET'])
def user_details(user_id):
    try:
        data = get_user_service_a(user_id)

        if not data:
            return jsonify({
                "error": f"User {user_id} not found"
            }), 404

        user = data.get('user')
        registration_date = datetime.fromisoformat(user['registration_date'])
        days_since_registration = (datetime.now() - registration_date).days
        hours_since_registration = (datetime.now() - registration_date).seconds // 3600

        details = {
            "id": user['id'],
            "name": user['name'],
            "email": user['email'],
            "profile": user['profile'].upper(),
            "status": {
                "active": user['active'],
                "label": "Active" if user['active'] else "Inactive"
            },
            "registration_time": {
                "days": days_since_registration,
                "hours": hours_since_registration,
                "formatted": f"{days_since_registration} days and {hours_since_registration} hours"
            },
            "complete_registration_date": user['registration_date'],
            "source": "Consumed from Service A",
            "timestamp": datetime.now().isoformat()
        }

        return jsonify(details), 200
    except Exception as error:
        return jsonify({"error": str(error)}), 500

@app.route('/api/services-status', methods=['GET'])
def services_status():
    try:
        start_time = time.time()
        response = requests.get(f"{SERVICE_A_URL}/health", timeout=5)
        response_time = (time.time() - start_time) * 1000

        if response.status_code == 200:
            service_a_info = response.json()
            status = "available"
        else:
            service_a_info = {"error": "Status not 200"}
            status = "unavailable"
    except Exception as error:
        service_a_info = {"error": str(error)}
        response_time = None
        status = "unavailable"

    return jsonify({
        "service_b": {
            "status": "healthy",
            "port": 5002
        },
        "service_a": {
            "url": SERVICE_A_URL,
            "status": status,
            "response_time_ms": response_time,
            "info": service_a_info
        },
        "timestamp": datetime.now().isoformat()
    }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=False)