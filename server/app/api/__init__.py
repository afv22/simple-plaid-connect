from flask import Blueprint

from .portfolio import bp as portfolio_bp
from .plaid_link import bp as plaid_link_bp

bp = Blueprint("api", __name__)

bp.register_blueprint(portfolio_bp, url_prefix="/portfolio")
bp.register_blueprint(plaid_link_bp, url_prefix="/link")
