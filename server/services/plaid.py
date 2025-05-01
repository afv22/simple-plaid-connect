import os
from dotenv import load_dotenv

import plaid
from plaid import Environment
from plaid.api import plaid_api

load_dotenv()

PLAID_CLIENT_ID = os.getenv("PLAID_CLIENT_ID")
PLAID_ENV = os.getenv("PLAID_ENV", "sandbox")

if PLAID_ENV == "production":
    host = Environment.Production
    PLAID_SECRET = os.getenv("PLAID_SECRET_PRODUCTION")
else:
    host = Environment.Sandbox
    PLAID_SECRET = os.getenv("PLAID_SECRET_SANDBOX")


def init_client():
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


client = init_client()
