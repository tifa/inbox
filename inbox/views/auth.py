from datetime import datetime

from fastapi.responses import RedirectResponse
from nicegui import app, ui

from inbox.service.auth import DATETIME_FORMAT, authenticated, clear_session


@ui.page("/login")
def login() -> RedirectResponse | None:
    def try_login() -> None:
        account = authenticated(username.value, password.value)
        if account is not None:
            app.storage.user.update(
                {
                    "username": username.value,
                    "authenticated": True,
                    "last_active": datetime.now().strftime(DATETIME_FORMAT),
                }
            )
            ui.navigate.to(app.storage.user.get("referrer_path", "/"))
        else:
            ui.notify("Wrong username or password", color="negative")

    if app.storage.user.get("authenticated", False):
        ui.navigate.to("/")
        return None

    with ui.card().classes("absolute-center"):
        username = ui.input("Username").on("keydown.enter", try_login)
        password = ui.input(
            "Password", password=True, password_toggle_button=True
        ).on("keydown.enter", try_login)
        ui.button("Log in", on_click=try_login)
    return None


@ui.page("/logout")
def logout() -> None:
    clear_session()
    ui.navigate.to("/login")
