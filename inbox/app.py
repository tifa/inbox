#!/usr/bin/env python3
import os
import secrets

from nicegui import app, ui

import inbox.views.admin  # noqa
import inbox.views.auth  # noqa
from inbox.database import initialize_db
from inbox.service.auth import AuthMiddleware

initialize_db()
app.add_middleware(AuthMiddleware)


if __name__ in {"__main__", "__mp_main__"}:
    storage_secret = secrets.token_hex(32)
    ui.run(
        host="0.0.0.0",
        port=8080,
        storage_secret=storage_secret,
        uvicorn_logging_level=(
            "info" if os.environ.get("DEBUG") == "true" else "warning"
        ),
        title="Mail Admin",
    )
