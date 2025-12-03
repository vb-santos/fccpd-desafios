from flask import Flask, jsonify, request
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime
import os

app = Flask(__name__)

DB_HOST = os.getenv('DB_HOST', 'db')
DB_USER = os.getenv('DB_USER', 'usuario')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'senha123')
DB_NAME = os.getenv('DB_NAME', 'aplicacao')
DB_PORT = os.getenv('DB_PORT', '5432')


def connect_database():
    try:
        connection = psycopg2.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            port=DB_PORT
        )
        return connection
    except Exception as error:
        print(f"Connection error: {error}")
        return None


@app.route('/users', methods=['GET'])
def list_users():
    connection = connect_database()
    if not connection:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        cursor.execute("SELECT * FROM usuarios ORDER BY id;")
        users = cursor.fetchall()
        cursor.close()
        connection.close()
        return jsonify([dict(user) for user in users])
    except Exception as error:
        connection.close()
        return jsonify({"error": str(error)}), 500


@app.route('/users', methods=['POST'])
def create_user():
    connection = connect_database()
    if not connection:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        data = request.get_json()
        name = data.get('nome')
        email = data.get('email')

        if not name or not email:
            return jsonify({"error": "Name and email are required"}), 400

        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO usuarios (nome, email) VALUES (%s, %s) RETURNING id, nome, email, data_criacao;",
            (name, email)
        )
        new_user = cursor.fetchone()
        connection.commit()
        cursor.close()
        connection.close()

        return jsonify({
            "id": new_user[0],
            "nome": new_user[1],
            "email": new_user[2],
            "data_criacao": new_user[3].isoformat()
        }), 201
    except Exception as error:
        connection.close()
        return jsonify({"error": str(error)}), 500


@app.route('/logs', methods=['GET'])
def list_logs():
    connection = connect_database()
    if not connection:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        cursor.execute("SELECT * FROM logs ORDER BY data_log DESC;")
        logs = cursor.fetchall()
        cursor.close()
        connection.close()
        return jsonify([dict(log) for log in logs])
    except Exception as error:
        connection.close()
        return jsonify({"error": str(error)}), 500


@app.route('/status', methods=['GET'])
def status():
    connection = connect_database()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT COUNT(*) FROM usuarios;")
            total_users = cursor.fetchone()[0]
            cursor.close()
            connection.close()

            return jsonify({
                "status": "ok",
                "database": "connected",
                "total_users": total_users,
                "timestamp": datetime.now().isoformat()
            })
        except Exception as error:
            connection.close()
            return jsonify({
                "status": "error",
                "database": "query_error",
                "error": str(error),
                "timestamp": datetime.now().isoformat()
            }), 500
    else:
        return jsonify({
            "status": "error",
            "database": "disconnected",
            "timestamp": datetime.now().isoformat()
        }), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)