from flask import Flask
from flask_cors import CORS

from .routes.api import bp as api_bp


def create_app() -> Flask:
    app = Flask(__name__)

    VALID_ORIGINS = [
        "http://localhost:8080",
        "http://127.0.0.1:8080",
        "http://client:8080",
        "http://0.0.0.0:8080",
    ]

    # Apply CORS to API blueprint with specific allowed origins
    CORS(api_bp, origins=VALID_ORIGINS, supports_credentials=True)

    app.register_blueprint(api_bp)

    app.add_url_rule("/", "root", lambda: "Hello, World!")

    return app
