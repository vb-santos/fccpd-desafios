from flask import Flask, jsonify, request
import requests
from datetime import datetime
import os

app = Flask(__name__)

USERS_SERVICE_URL = os.getenv('USERS_SERVICE_URL', 'http://localhost:5001')
ORDERS_SERVICE_URL = os.getenv('ORDERS_SERVICE_URL', 'http://localhost:5002')
REQUEST_TIMEOUT = 5


def make_request(method, url, data=None, params=None):
    try:
        if method == 'GET':
            response = requests.get(url, params=params, timeout=REQUEST_TIMEOUT)
        elif method == 'POST':
            response = requests.post(url, json=data, timeout=REQUEST_TIMEOUT)
        elif method == 'PUT':
            response = requests.put(url, json=data, timeout=REQUEST_TIMEOUT)
        elif method == 'DELETE':
            response = requests.delete(url, timeout=REQUEST_TIMEOUT)
        else:
            return {"error": "HTTP method not supported"}, 400

        if response.status_code == 204:
            return {}, 204

        try:
            response_data = response.json()
        except Exception:
            response_data = {"message": response.text}

        return response_data, response.status_code

    except requests.exceptions.Timeout:
        return {"error": f"Timeout connecting to service: {url}"}, 504
    except requests.exceptions.ConnectionError:
        return {"error": f"Error connecting to service: {url}"}, 503
    except Exception as error:
        return {"error": f"Request error: {str(error)}"}, 500


def check_services():
    try:
        users_response = requests.get(f"{USERS_SERVICE_URL}/health", timeout=REQUEST_TIMEOUT)
        orders_response = requests.get(f"{ORDERS_SERVICE_URL}/health", timeout=REQUEST_TIMEOUT)

        return {
            "users": users_response.status_code == 200,
            "orders": orders_response.status_code == 200
        }
    except Exception:
        return {
            "users": False,
            "orders": False
        }

@app.route('/health', methods=['GET'])
def health():
    services = check_services()
    status_value = "healthy" if all(services.values()) else "degraded"

    return jsonify({
        "status": status_value,
        "service": "API Gateway",
        "services": services,
        "timestamp": datetime.now().isoformat()
    }), 200

@app.route('/users', methods=['GET'])
def gateway_list_users():
    params = {}
    if request.args.get('active'):
        params['active'] = request.args.get('active')
    if request.args.get('profile'):
        params['profile'] = request.args.get('profile')

    data, status_code = make_request(
        'GET',
        f"{USERS_SERVICE_URL}/api/users",
        params=params
    )

    return jsonify(data), status_code


@app.route('/users/<int:user_id>', methods=['GET'])
def gateway_get_user(user_id):
    data, status_code = make_request(
        'GET',
        f"{USERS_SERVICE_URL}/api/users/{user_id}"
    )

    return jsonify(data), status_code


@app.route('/users', methods=['POST'])
def gateway_create_user():
    input_data = request.get_json()

    data, status_code = make_request(
        'POST',
        f"{USERS_SERVICE_URL}/api/users",
        data=input_data
    )

    return jsonify(data), status_code


@app.route('/users/<int:user_id>', methods=['PUT'])
def gateway_update_user(user_id):
    input_data = request.get_json()

    data, status_code = make_request(
        'PUT',
        f"{USERS_SERVICE_URL}/api/users/{user_id}",
        data=input_data
    )

    return jsonify(data), status_code


@app.route('/users/<int:user_id>', methods=['DELETE'])
def gateway_delete_user(user_id):
    data, status_code = make_request(
        'DELETE',
        f"{USERS_SERVICE_URL}/api/users/{user_id}"
    )

    return jsonify(data), status_code


@app.route('/users/stats', methods=['GET'])
def gateway_users_stats():
    data, status_code = make_request(
        'GET',
        f"{USERS_SERVICE_URL}/api/users/statistics/summary"
    )

    return jsonify(data), status_code

@app.route('/orders', methods=['GET'])
def gateway_list_orders():
    params = {}
    if request.args.get('user_id'):
        params['user_id'] = request.args.get('user_id')
    if request.args.get('status'):
        params['status'] = request.args.get('status')

    data, status_code = make_request(
        'GET',
        f"{ORDERS_SERVICE_URL}/api/orders",
        params=params
    )

    return jsonify(data), status_code


@app.route('/orders/<int:order_id>', methods=['GET'])
def gateway_get_order(order_id):
    data, status_code = make_request(
        'GET',
        f"{ORDERS_SERVICE_URL}/api/orders/{order_id}"
    )

    return jsonify(data), status_code


@app.route('/orders', methods=['POST'])
def gateway_create_order():
    input_data = request.get_json()

    data, status_code = make_request(
        'POST',
        f"{ORDERS_SERVICE_URL}/api/orders",
        data=input_data
    )

    return jsonify(data), status_code


@app.route('/orders/<int:order_id>', methods=['PUT'])
def gateway_update_order(order_id):
    input_data = request.get_json()

    data, status_code = make_request(
        'PUT',
        f"{ORDERS_SERVICE_URL}/api/orders/{order_id}",
        data=input_data
    )

    return jsonify(data), status_code


@app.route('/orders/<int:order_id>', methods=['DELETE'])
def gateway_delete_order(order_id):
    data, status_code = make_request(
        'DELETE',
        f"{ORDERS_SERVICE_URL}/api/orders/{order_id}"
    )

    return jsonify(data), status_code


@app.route('/orders/user/<int:user_id>', methods=['GET'])
def gateway_user_orders(user_id):
    data, status_code = make_request(
        'GET',
        f"{ORDERS_SERVICE_URL}/api/orders/user/{user_id}"
    )

    return jsonify(data), status_code


@app.route('/orders/stats', methods=['GET'])
def gateway_orders_stats():
    data, status_code = make_request(
        'GET',
        f"{ORDERS_SERVICE_URL}/api/orders/statistics/summary"
    )

    return jsonify(data), status_code

@app.route('/dashboard', methods=['GET'])
def gateway_dashboard():
    users_response, users_status = make_request(
        'GET',
        f"{USERS_SERVICE_URL}/api/users/statistics/summary"
    )

    orders_response, orders_status = make_request(
        'GET',
        f"{ORDERS_SERVICE_URL}/api/orders/statistics/summary"
    )

    if users_status != 200 or orders_status != 200:
        return jsonify({
            "error": "Error getting service data",
            "users_status": users_status,
            "orders_status": orders_status
        }), 503

    return jsonify({
        "title": "Users and Orders Dashboard",
        "users": users_response,
        "orders": orders_response,
        "timestamp": datetime.now().isoformat()
    }), 200


@app.route('/users-with-orders', methods=['GET'])
def gateway_users_with_orders():
    try:
        users_response, users_status = make_request(
            'GET',
            f"{USERS_SERVICE_URL}/api/users"
        )

        if users_status != 200:
            return jsonify({"error": "Error getting users"}), users_status

        users = users_response.get('users', [])
        result = []

        for user in users:
            user_id = user['id']
            orders_response, orders_status = make_request(
                'GET',
                f"{ORDERS_SERVICE_URL}/api/orders/user/{user_id}"
            )

            user_with_orders = {
                "user": user,
                "orders": orders_response.get('orders', []) if orders_status == 200 else [],
                "total_orders": orders_response.get('total_orders', 0) if orders_status == 200 else 0,
                "total_order_value": orders_response.get('total_value', 0) if orders_status == 200 else 0
            }
            result.append(user_with_orders)

        return jsonify({
            "total_users": len(users),
            "users_with_orders": result,
            "timestamp": datetime.now().isoformat()
        }), 200

    except Exception as error:
        return jsonify({"error": str(error)}), 500

@app.route('/', methods=['GET'])
def documentation():
    return jsonify({
        "title": "API Gateway - Microservices Architecture",
        "version": "1.0.0",
        "description": "Gateway centralizing access to user and order microservices",
        "endpoints": {
            "health": {
                "GET /health": "Health check for gateway and its services"
            },
            "users": {
                "GET /users": "List all users",
                "GET /users/<id>": "Get user details",
                "POST /users": "Create new user",
                "PUT /users/<id>": "Update user",
                "DELETE /users/<id>": "Delete user",
                "GET /users/stats": "User statistics"
            },
            "orders": {
                "GET /orders": "List all orders",
                "GET /orders/<id>": "Get order details",
                "GET /orders/user/<user_id>": "List user orders",
                "POST /orders": "Create new order",
                "PUT /orders/<id>": "Update order",
                "DELETE /orders/<id>": "Cancel order",
                "GET /orders/stats": "Order statistics"
            },
            "composition": {
                "GET /dashboard": "Consolidated dashboard",
                "GET /users-with-orders": "Users with their orders"
            }
        },
        "internal_services": {
            "users_service": USERS_SERVICE_URL,
            "orders_service": ORDERS_SERVICE_URL
        }
    }), 200


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "error": "Route not found",
        "message": "Visit GET / for documentation",
        "timestamp": datetime.now().isoformat()
    }), 404


@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({
        "error": "Method not allowed",
        "timestamp": datetime.now().isoformat()
    }), 405


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)