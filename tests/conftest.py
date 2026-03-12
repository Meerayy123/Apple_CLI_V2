from __future__ import annotations

import sys
from pathlib import Path
import os
from typing import Generator

project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

import pytest
from flask import Flask
from sqlalchemy import event

from app import create_app, cache
from app.config import get_config
from app.db import db as _db
from app.models import Security, User


@pytest.fixture(scope='session')
def app() -> Generator[Flask, None, None]:
    # create a Flask test app using the test config
    config = get_config('test')
    app = create_app(config)

    # ensure the cache uses a simple in-memory backend for tests
    app.config['CACHE_TYPE'] = 'SimpleCache'
    cache.init_app(app)

    # create tables
    with app.app_context():
        _db.create_all()

    yield app

    # teardown
    with app.app_context():
        _db.drop_all()


@pytest.fixture(scope='function')
def client(app: Flask):
    with app.test_client() as client:
        yield client


@pytest.fixture(scope='function')
def db_session(app: Flask) -> Generator:
    """Provide a transactional scope around a series of operations for tests."""
    # push an application context so Flask-SQLAlchemy can access the app
    ctx = app.app_context()
    ctx.push()

    connection = _db.engine.connect()
    trans = connection.begin()

    options = dict(bind=connection, binds={})
    sess = _db.create_scoped_session(options=options)

    # override the session used by the app
    _db.session = sess

    try:
        # seed some data
        admin_user = User(username='admin', password='admin', firstname='Admin', lastname='User', balance=1000.00)
        sess.add(admin_user)

        securities = [
            Security(ticker='AAPL', issuer='Apple Inc.', price=150.00),
            Security(ticker='GOOGL', issuer='Alphabet Inc.', price=2800.00),
            Security(ticker='MSFT', issuer='Microsoft Corp.', price=300.00),
        ]
        sess.add_all(securities)
        sess.commit()

        yield sess

    finally:
        trans.rollback()
        connection.close()
    _db.session.remove()
    # pop the app context
    ctx.pop()
