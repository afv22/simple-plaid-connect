from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS

from server.routes.api import bp as api_bp

load_dotenv()

app = Flask(__name__)
CORS(app)

app.register_blueprint(api_bp)
