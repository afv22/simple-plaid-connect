from flask import Blueprint

from plaid.model.accounts_get_request import AccountsGetRequest

from google.cloud.firestore_v1.base_query import FieldFilter

from app.session import get_session
from app.services.firestore import client as fs_client
from app.services.plaid import get_plaid_client
from app.services.email import EmailClientWrapper
from app.generate_email import generate_email
from app.get_holdings import get_holdings
from app.get_rebalance_amounts import get_rebalance_amounts, TARGET_ALLOCATIONS
from app.utils import error_handler
from app.services.auth import require_token

bp = Blueprint("portfolio", __name__)


@bp.route("/holdings")
@require_token
@error_handler
def holdings():
    return list(map(lambda h: h.symbol, get_holdings()))


@bp.get("/accounts")
@require_token
@error_handler
def get_accounts():
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
    return accounts


@bp.route("/rebalance_amounts")
@require_token
@error_handler
def rebalance_amounts():
    holdings = get_holdings()
    return get_rebalance_amounts(holdings).to_json()


@bp.route("/check_allocation")
@require_token
@error_handler
def check_allocation():
    holdings = get_holdings()
    rebalance_amounts = get_rebalance_amounts(holdings)

    need_rebalance = False
    for _, asset in rebalance_amounts.iterrows():
        if abs(asset["absolute_difference"]) >= 0.05:  # type: ignore
            need_rebalance = True
            break
        if abs(asset["relative_difference"]) >= 0.25:  # type: ignore
            need_rebalance = True
            break

    if not need_rebalance:
        return {"status": "rebalance_not_required"}

    EmailClientWrapper.send("Time to rebalance!", generate_email(rebalance_amounts))
    return {"status": "rebalance_required"}


@bp.route("/target_allocation")
@require_token
@error_handler
def target_allocation():
    return TARGET_ALLOCATIONS
