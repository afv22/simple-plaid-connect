from flask import session

from typing import TypedDict


class SessionData(TypedDict):
    uid: str


def get_session() -> SessionData:
    return session  # type: ignore
