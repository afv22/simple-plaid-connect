import os
import json
import time
from dotenv import load_dotenv

from flask import Blueprint, request, jsonify

import plaid
from plaid.model.country_code import CountryCode
from plaid.model.item_public_token_exchange_request import (
    ItemPublicTokenExchangeRequest,
)
from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
from plaid.model.accounts_get_request import AccountsGetRequest
from plaid.model.products import Products

from server.services.firestore import client as fs_client
from server.services.plaid import client as plaid_client, host

load_dotenv()

bp = Blueprint("api", __name__, url_prefix="/api")

PLAID_PRODUCTS = os.getenv("PLAID_PRODUCTS", "").split(",")
PLAID_COUNTRY_CODES = os.getenv("PLAID_COUNTRY_CODES", "US").split(",")

user_id = 1 if host == plaid.Environment.Sandbox else 2


@bp.get("/create_link_token")
def create_link_token():
    try:
        link_request = LinkTokenCreateRequest(
            products=list(map(lambda x: Products(x), PLAID_PRODUCTS)),
            client_name="Plaid Connect",
            country_codes=list(map(lambda x: CountryCode(x), PLAID_COUNTRY_CODES)),
            language="en",
            user=LinkTokenCreateRequestUser(client_user_id=str(time.time())),
        )
        link_response = plaid_client.link_token_create(link_request)
        return jsonify(link_response.to_dict())
    except plaid.ApiException as e:
        return json.loads(e.body)


@bp.post("/exchange_public_token")
def exchange_public_token():
    public_token = request.json["public_token"]
    try:
        exchange_request = ItemPublicTokenExchangeRequest(public_token=public_token)
        exchange_response = plaid_client.item_public_token_exchange(exchange_request)
        access_token = exchange_response["access_token"]
        item_id = exchange_response["item_id"]
        fs_client.Items.add({"access_token": access_token, "user_id": user_id}, item_id)
        return jsonify(exchange_response.to_dict())
    except plaid.ApiException as e:
        return json.loads(e.body)


@bp.get("/accounts")
def get_accounts():
    try:
        connections = fs_client.Items.where("user_id", "==", user_id).get()
        accounts = []
        for connection in connections:
            access_token = connection.get("access_token")
            accounts_request = AccountsGetRequest(access_token=access_token)
            accounts_response = plaid_client.accounts_get(accounts_request)
            for account in accounts_response["accounts"]:
                name = account["name"]
                balance = account["balances"]["current"]
                accounts.append({"name": name, "balance": balance})
        return jsonify(accounts)
    except plaid.ApiException as e:
        return json.loads(e.body)
