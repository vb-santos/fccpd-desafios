from flask import Flask, jsonify, request
import redis
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime
import os
import json

app = Flask(__name__)

DB_HOST = os.getenv('DB_HOST', 'db')
DB_USER = os.getenv('DB_USER', 'usuario')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'senha123')
DB_NAME = os.getenv('DB_NAME', 'aplicacao')
DB_PORT = os.getenv('DB_PORT', '5432')

REDIS_HOST = os.getenv('REDIS_HOST', 'cache')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))


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
        print(f"Error connecting to DB: {error}")
        return None


def connect_redis():
    try:
        redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
        redis_client.ping()
        return redis_client
    except Exception as error:
        print(f"Error connecting to Redis: {error}")
        return None


@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy"}), 200


@app.route('/status', methods=['GET'])
def status():
    db_connection = connect_database()
    redis_connection = connect_redis()

    db_status = "connected" if db_connection else "disconnected"
    redis_status = "connected" if redis_connection else "disconnected"

    # Close connections if opened
    if db_connection:
        db_connection.close()
    if redis_connection:
        redis_connection.close()

    return jsonify({
        "status": "ok",
        "database": db_status,
        "cache": redis_status,
        "timestamp": datetime.now().isoformat()
    }), 200


@app.route('/api/posts', methods=['GET'])
def list_posts():
    connection = connect_database()
    if not connection:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        cursor.execute("SELECT * FROM posts ORDER BY id DESC;")
        posts = cursor.fetchall()
        cursor.close()
        connection.close()
        return jsonify([dict(post) for post in posts])
    except Exception as error:
        connection.close()
        return jsonify({"error": str(error)}), 500


@app.route('/api/posts', methods=['POST'])
def create_post():
    connection = connect_database()
    if not connection:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        data = request.get_json()
        title = data.get('titulo')
        content = data.get('conteudo')
        author = data.get('autor', 'Anônimo')

        if not title or not content:
            return jsonify({"error": "Title and content are required"}), 400

        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO posts (title, content, author) VALUES (%s, %s, %s) RETURNING id, title, content, author, created_at;",
            (title, content, author)
        )
        new_post = cursor.fetchone()
        connection.commit()
        cursor.close()
        connection.close()

        redis_client = connect_redis()
        if redis_client:
            redis_client.delete('posts_cache')

        return jsonify({
            "id": new_post[0],
            "titulo": new_post[1],
            "conteudo": new_post[2],
            "autor": new_post[3],
            "data_criacao": new_post[4].isoformat()
        }), 201
    except Exception as error:
        connection.close()
        return jsonify({"error": str(error)}), 500


@app.route('/api/posts/cache', methods=['GET'])
def list_posts_cache():
    redis_client = connect_redis()

    if redis_client:
        cached_data = redis_client.get('posts_cache')
        if cached_data:
            return jsonify({
                "source": "cache",
                "data": json.loads(cached_data),
                "timestamp": datetime.now().isoformat()
            }), 200

    connection = connect_database()
    if not connection:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        cursor.execute("SELECT * FROM posts ORDER BY id DESC;")
        posts = cursor.fetchall()
        cursor.close()
        connection.close()

        posts_list = [dict(post) for post in posts]

        if redis_client:
            redis_client.setex('posts_cache', 60, json.dumps(posts_list, default=str))

        return jsonify({
            "source": "database",
            "data": posts_list,
            "timestamp": datetime.now().isoformat()
        }), 200
    except Exception as error:
        connection.close()
        return jsonify({"error": str(error)}), 500


@app.route('/api/counter', methods=['GET'])
def counter():
    redis_client = connect_redis()
    if not redis_client:
        return jsonify({"error": "Cache not available"}), 500

    try:
        current_counter = redis_client.incr('request_counter')
        return jsonify({
            "counter": current_counter,
            "message": f"Request number {current_counter}",
            "timestamp": datetime.now().isoformat()
        }), 200
    except Exception as error:
        return jsonify({"error": str(error)}), 500


@app.route('/api/stats', methods=['GET'])
def stats():
    connection = connect_database()
    redis_client = connect_redis()

    total_posts = 0
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT COUNT(*) FROM posts;")
            total_posts = cursor.fetchone()[0]
            cursor.close()
            connection.close()
        except Exception:
            pass

    total_requests = 0
    if redis_client:
        try:
            total_requests = int(redis_client.get('request_counter') or 0)
        except Exception:
            pass

    return jsonify({
        "total_posts": total_posts,
        "total_requests": total_requests,
        "timestamp": datetime.now().isoformat()
    }), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)