from nicegui import ui

from inbox.views.auth import logout
from inbox.views.reject_sender import reject_sender
from inbox.views.domain import domain
from inbox.views.email import email


def header() -> None:
    with ui.header().classes("items-center justify-between"):
        ui.avatar("favorite_border")
        nav = [
            ("Emails", "/emails", "alternate_email"),
            ("Domains", "/domains", "dns"),
            ("Deny From", "/deny-from", "block"),
        ]
        with ui.row().classes("max-sm:hidden"):
            for title, path, icon in nav:
                ui.button(title, icon=icon).props("flat color=white").on(
                    "click", lambda p=path: ui.navigate.to(p)
                )
        with ui.row().classes("sm:hidden"):
            for title, path, icon in nav:
                ui.button(icon=icon).props("flat color=white").on(
                    "click", lambda p=path: ui.navigate.to(p)
                )
        with ui.button(on_click=logout, icon="logout").props("flat color=white"):
            ui.tooltip("Logout")


@ui.page("/")
@ui.page("/emails")
def main_page() -> None:
    header()
    email()


@ui.page("/domains")
def domains_page() -> None:
    header()
    domain()


@ui.page("/deny-from")
def deny_from_page() -> None:
    header()
    reject_sender()
