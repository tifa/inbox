import logging

from nicegui import ui

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


def notify_error(message: str, debug: str | None = None) -> None:
    ui.notify(message, color="negative")
    if debug:
        log.error(f"{message}: {debug}")


def notify_success(message: str, debug: str | None = None) -> None:
    ui.notify(message, color="positive")
    if debug:
        log.debug(f"{message}: {debug}")


def notify_info(message: str, debug: str | None = None) -> None:
    ui.notify(message, color="info")
    if debug:
        log.debug(f"{message}: {debug}")
