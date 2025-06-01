import os
import plaid
from plaid import Environment
from plaid.api import plaid_api

_client = None

def get_plaid_client():
    global _client
    if _client is None:
        _client = _init_client()
    return _client

def _init_client():
    PLAID_CLIENT_ID = os.getenv("PLAID_CLIENT_ID")
    PLAID_ENV = os.getenv("PLAID_ENV", "sandbox")
    
    if PLAID_ENV == "production":
        host = Environment.Production
        PLAID_SECRET = os.getenv("PLAID_SECRET_PRODUCTION")
    else:
        host = Environment.Sandbox
        PLAID_SECRET = os.getenv("PLAID_SECRET_SANDBOX")
    
    configuration = plaid.Configuration(
        host=host,
        api_key={
            "clientId": PLAID_CLIENT_ID,
            "secret": PLAID_SECRET,
            "plaidVersion": "2020-09-14",
        },
    )
    api_client = plaid.ApiClient(configuration)
    return plaid_api.PlaidApi(api_client)