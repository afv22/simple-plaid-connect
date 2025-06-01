import os
import json

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

from app.session import get_session
from app.services.firestore import client as fs_client
from app.services.plaid import get_plaid_client
from app.services.auth import token_required

from google.cloud.firestore_v1.base_query import FieldFilter

bp = Blueprint("api", __name__, url_prefix="/api")


@bp.get("/create_link_token")
@token_required
def create_link_token():
    try:
        plaid_products = os.getenv("PLAID_PRODUCTS", "").split(",")
        plaid_country_codes = os.getenv("PLAID_COUNTRY_CODES", "US").split(",")
        link_request = LinkTokenCreateRequest(
            products=list(map(Products, plaid_products)),
            client_name="Plaid Connect",
            country_codes=list(map(lambda x: CountryCode(x), plaid_country_codes)),
            language="en",
            user=LinkTokenCreateRequestUser(client_user_id=get_session()["uid"]),
        )
        link_response = get_plaid_client().link_token_create(link_request)
        return jsonify(link_response.to_dict())
    except plaid.ApiException as e:
        return json.loads(e.body) if e.body is not None else jsonify({"error": str(e)})


@bp.post("/exchange_public_token")
@token_required
def exchange_public_token():
    try:
        plaid_client = get_plaid_client()
        public_token = request.get_json()["public_token"]
        exchange_request = ItemPublicTokenExchangeRequest(public_token=public_token)
        exchange_response = plaid_client.item_public_token_exchange(exchange_request)
        access_token = exchange_response["access_token"]
        item_id = exchange_response["item_id"]
        fs_client.Items.add(
            {"access_token": access_token, "user_id": get_session()["uid"]}, item_id
        )
        return jsonify(exchange_response.to_dict())
    except plaid.ApiException as e:
        return json.loads(e.body) if e.body is not None else jsonify({"error": str(e)})


@bp.get("/accounts")
@token_required
def get_accounts():
    try:
        is_user_filter = FieldFilter("user_id", "==", get_session()["uid"])
        connections = fs_client.Items.where(filter=is_user_filter).get()
        accounts = []
        for connection in connections:
            access_token = connection.get("access_token")
            accounts_request = AccountsGetRequest(access_token=access_token)
            accounts_response = get_plaid_client().accounts_get(accounts_request)
            for account in accounts_response["accounts"]:
                name = account["name"]
                balance = account["balances"]["current"]
                accounts.append({"name": name, "balance": balance})
        return jsonify(accounts)
    except plaid.ApiException as e:
        return json.loads(e.body) if e.body is not None else jsonify({"error": str(e)})
