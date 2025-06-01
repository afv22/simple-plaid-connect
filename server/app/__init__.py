import os

from flask import Flask
from flask_cors import CORS

from .api import bp as api_bp


def create_app() -> Flask:
    app = Flask(__name__)
    app.secret_key = os.getenv("FLASK_SECRET_KEY")

    if not app.secret_key:
        raise RuntimeError("Secret key not set")

    VALID_ORIGINS = [
        "http://localhost:8080",
        "http://127.0.0.1:8080",
        "http://client:8080",
        "http://0.0.0.0:8080",
    ]

    CORS(app, origins=VALID_ORIGINS, supports_credentials=True)

    app.register_blueprint(api_bp, url_prefix="/api")

    app.add_url_rule("/", "root", lambda: "Hello, World!")

    return app
