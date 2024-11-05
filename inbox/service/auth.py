from datetime import datetime

from argon2 import PasswordHasher
from fastapi import Request
from fastapi.responses import RedirectResponse
from nicegui import app
from starlette.middleware.base import BaseHTTPMiddleware

from inbox.model import Account

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S.%f"
UNRESTRICTED_PAGE_ROUTES = {"/login", "/_nicegui"}


class AuthMiddleware(BaseHTTPMiddleware):
    """This middleware restricts access to all NiceGUI pages.

    It redirects the user to the login page if they are not authenticated.
    """

    def is_session_expired(self) -> bool:
        try:
            last_active_str = app.storage.user["last_active"]
            last_active = datetime.strptime(last_active_str, DATETIME_FORMAT)
            return (datetime.now() - last_active).days >= 1
        except (KeyError, TypeError, ValueError):
            return True

    async def dispatch(self, request: Request, call_next):
        if not app.storage.user.get("authenticated", False):
            if not any(
                request.url.path.startswith(route)
                for route in UNRESTRICTED_PAGE_ROUTES
            ):
                app.storage.user["referrer_path"] = request.url.path
                return RedirectResponse("/login")
        elif self.is_session_expired():
            clear_session()
            return RedirectResponse("/login")
        else:
            app.storage.user["last_active"] = datetime.now().strftime(
                DATETIME_FORMAT
            )
        return await call_next(request)


def clear_session() -> None:
    app.storage.user.clear()


def authenticated(username: str, password: str) -> Account | None:
    account = Account.get_or_none(Account.username == username)
    if account is None:
        return None
    if PasswordHasher().verify(account.password, password):
        return account
    return None


def active_account() -> Account | None:
    if not app.storage.user.get("authenticated", False):
        return None
    username = app.storage.user.get("username")
    if not username:
        return None
    return Account.get_or_none(Account.username == username)
