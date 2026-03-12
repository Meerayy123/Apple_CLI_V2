from typing import Any

from app.db import db


def get_session() -> Any:
    """Return the current SQLAlchemy session.

This shim allows tests to monkeypatch `app.database.get_session`.
"""
    return db.session
from app.db import db


def get_session():
    """Return the current SQLAlchemy session (shim for tests).

    Tests monkeypatch `app.database.get_session` to simulate failures; this
    shim delegates to the Flask-SQLAlchemy `db.session`.
    """
    return db.session
