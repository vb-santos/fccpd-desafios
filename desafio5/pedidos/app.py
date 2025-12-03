from flask import Flask, jsonify, request
from datetime import datetime, timedelta

app = Flask(__name__)

ORDERS = [
    {
        "id": 101,
        "user_id": 1,
        "order_date": (datetime.now() - timedelta(days=30)).isoformat(),
        "status": "delivered",
        "total": 299.90,
        "items": [
            {"product": "Laptop", "quantity": 1, "price": 299.90}
        ]
    },
    {
        "id": 102,
        "user_id": 2,
        "order_date": (datetime.now() - timedelta(days=15)).isoformat(),
        "status": "processing",
        "total": 89.50,
        "items": [
            {"product": "Mouse", "quantity": 2, "price": 44.75}
        ]
    },
    {
        "id": 103,
        "user_id": 4,
        "order_date": (datetime.now() - timedelta(days=5)).isoformat(),
        "status": "delivered",
        "total": 150.00,
        "items": [
            {"product": "Keyboard", "quantity": 1, "price": 150.00}
        ]
    },
    {
        "id": 104,
        "user_id": 5,
        "order_date": (datetime.now() - timedelta(days=2)).isoformat(),
        "status": "shipped",
        "total": 49.99,
        "items": [
            {"product": "Headset", "quantity": 1, "price": 49.99}
        ]
    },
    {
        "id": 105,
        "user_id": 1,
        "order_date": datetime.now().isoformat(),
        "status": "pending",
        "total": 199.99,
        "items": [
            {"product": "Monitor 27\"", "quantity": 1, "price": 199.99}
        ]
    }
]


@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        "status": "healthy",
        "service": "Orders Microservice",
        "timestamp": datetime.now().isoformat()
    }), 200


@app.route('/api/orders', methods=['GET'])
def list_orders():
    try:
        orders = ORDERS.copy()

        user_id_param = request.args.get('user_id')
        if user_id_param:
            try:
                user_id_int = int(user_id_param)
                orders = [order for order in orders if order['user_id'] == user_id_int]
            except ValueError:
                return jsonify({"error": "user_id must be a number"}), 400

        status_param = request.args.get('status')
        if status_param:
            orders = [order for order in orders if order['status'].lower() == status_param.lower()]

        return jsonify({
            "total": len(orders),
            "orders": orders,
            "timestamp": datetime.now().isoformat()
        }), 200
    except Exception as error:
        return jsonify({"error": str(error)}), 500


@app.route('/api/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    try:
        order = next((order for order in ORDERS if order['id'] == order_id), None)
        if not order:
            return jsonify({"error": f"Order {order_id} not found"}), 404

        return jsonify({
            "order": order,
            "timestamp": datetime.now().isoformat()
        }), 200
    except Exception as error:
        return jsonify({"error": str(error)}), 500


@app.route('/api/orders', methods=['POST'])
def create_order():
    try:
        data = request.get_json()

        if not data or 'user_id' not in data or 'items' not in data:
            return jsonify({"error": "user_id and items are required"}), 400

        if not isinstance(data['items'], list) or len(data['items']) == 0:
            return jsonify({"error": "items must be a non-empty list"}), 400

        new_id = max([order['id'] for order in ORDERS]) + 1

        total = sum(item.get('quantity', 1) * item.get('price', 0) for item in data['items'])

        new_order = {
            "id": new_id,
            "user_id": data['user_id'],
            "order_date": datetime.now().isoformat(),
            "status": "pending",
            "total": round(total, 2),
            "items": data['items']
        }

        ORDERS.append(new_order)

        return jsonify({
            "message": "Order created successfully",
            "order": new_order,
            "timestamp": datetime.now().isoformat()
        }), 201
    except Exception as error:
        return jsonify({"error": str(error)}), 500


@app.route('/api/orders/<int:order_id>', methods=['PUT'])
def update_order(order_id):
    try:
        order = next((order for order in ORDERS if order['id'] == order_id), None)
        if not order:
            return jsonify({"error": f"Order {order_id} not found"}), 404

        data = request.get_json()

        if 'status' in data:
            valid_statuses = ['pending', 'processing', 'shipped', 'delivered', 'cancelled']
            if data['status'] not in valid_statuses:
                return jsonify({"error": f"Invalid status. Valid: {valid_statuses}"}), 400
            order['status'] = data['status']

        return jsonify({
            "message": "Order updated successfully",
            "order": order,
            "timestamp": datetime.now().isoformat()
        }), 200
    except Exception as error:
        return jsonify({"error": str(error)}), 500


@app.route('/api/orders/<int:order_id>', methods=['DELETE'])
def cancel_order(order_id):
    try:
        order = next((order for order in ORDERS if order['id'] == order_id), None)
        if not order:
            return jsonify({"error": f"Order {order_id} not found"}), 404

        if order['status'] == 'delivered':
            return jsonify({"error": "Cannot cancel delivered order"}), 409

        order['status'] = 'cancelled'

        return jsonify({
            "message": f"Order {order_id} cancelled successfully",
            "order": order,
            "timestamp": datetime.now().isoformat()
        }), 200
    except Exception as error:
        return jsonify({"error": str(error)}), 500


@app.route('/api/orders/user/<int:user_id>', methods=['GET'])
def list_user_orders(user_id):
    try:
        user_orders = [order for order in ORDERS if order['user_id'] == user_id]

        return jsonify({
            "user_id": user_id,
            "total_orders": len(user_orders),
            "orders": user_orders,
            "total_value": round(sum(order['total'] for order in user_orders), 2),
            "timestamp": datetime.now().isoformat()
        }), 200
    except Exception as error:
        return jsonify({"error": str(error)}), 500


@app.route('/api/orders/statistics/summary', methods=['GET'])
def order_statistics():
    try:
        total = len(ORDERS)
        total_value = sum(order['total'] for order in ORDERS)

        status_distribution = {}
        for order in ORDERS:
            status = order['status']
            status_distribution[status] = status_distribution.get(status, 0) + 1

        return jsonify({
            "total_orders": total,
            "total_value": round(total_value, 2),
            "average_value": round(total_value / total, 2) if total > 0 else 0,
            "status_distribution": status_distribution,
            "timestamp": datetime.now().isoformat()
        }), 200
    except Exception as error:
        return jsonify({"error": str(error)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=False)