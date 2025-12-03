from flask import Flask, jsonify
from datetime import datetime
from typing import Dict, Any

app = Flask(__name__)


@app.route('/')
def index() -> str:
    current_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f"Servidor web ativo! Timestamp: {current_timestamp}\n"


@app.route('/status')
def status() -> Dict[str, Any]:
    return {
        "status": "ok",
        "servico": "servidor-web"
    }


def main() -> None:
    """Start the Flask application."""
    app.run(host='0.0.0.0', port=8080, debug=False)


if __name__ == '__main__':
    main()