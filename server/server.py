import os
import json
import time

from dotenv import load_dotenv
from flask import Blueprint, Flask, request, jsonify
from flask_cors import CORS

import plaid
from plaid.model.country_code import CountryCode
from plaid.model.item_public_token_exchange_request import (
    ItemPublicTokenExchangeRequest,
)
from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
from plaid.model.accounts_get_request import AccountsGetRequest
from plaid.model.products import Products

from server.db import fs_client
from server.plaid_client import client

load_dotenv()


app = Flask(__name__)
CORS(app)

api_bp = Blueprint('api', __name__, url_prefix='/api')

PLAID_PRODUCTS = os.getenv("PLAID_PRODUCTS", "").split(",")
PLAID_COUNTRY_CODES = os.getenv("PLAID_COUNTRY_CODES", "US").split(",")

products = []
for product in PLAID_PRODUCTS:
    products.append(Products(product))


@api_bp.get("/create_link_token")
def create_link_token():
    try:
        request = LinkTokenCreateRequest(
            products=products,
            client_name="Plaid Connect",
            country_codes=list(map(lambda x: CountryCode(x), PLAID_COUNTRY_CODES)),
            language="en",
            user=LinkTokenCreateRequestUser(client_user_id=str(time.time())),
        )
        response = client.link_token_create(request)
        return jsonify(response.to_dict())
    except plaid.ApiException as e:
        return json.loads(e.body)


@api_bp.post("/exchange_public_token")
def exchange_public_token():
    public_token = request.json["public_token"]
    try:
        exchange_request = ItemPublicTokenExchangeRequest(public_token=public_token)
        exchange_response = client.item_public_token_exchange(exchange_request)
        access_token = exchange_response["access_token"]
        item_id = exchange_response["item_id"]
        fs_client.Items.add({"access_token": access_token}, item_id)
        return jsonify(exchange_response.to_dict())
    except plaid.ApiException as e:
        return json.loads(e.body)


@api_bp.get("/accounts")
def get_accounts():
    try:
        connections = fs_client.Items.get()
        accounts = []
        for connection in connections:
            request = AccountsGetRequest(access_token=connection.get("access_token"))
            response = client.accounts_get(request)
            for account in response["accounts"]:
                accounts.append(
                    {"name": account["name"], "balance": account["balances"]["current"]}
                )
        return jsonify(accounts)
    except plaid.ApiException as e:
        return json.loads(e.body)
