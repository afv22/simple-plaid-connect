from flask import Flask
from flask_cors import CORS

from server.routes.api import bp as api_bp

app = Flask(__name__)

VALID_ORIGINS = ["localhost:8080", "127.0.0.1:8080"]

CORS(api_bp, origins=[f"https?://{origin}(/|$).*" for origin in VALID_ORIGINS])

app.register_blueprint(api_bp)
