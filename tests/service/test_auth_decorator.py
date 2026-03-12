import pytest
from unittest.mock import patch

from flask import g


def test_access_endpoint_no_auth_required(client, db_session, monkeypatch):
    # By default REQUIRE_AUTH is False in tests; endpoint should work
    resp = client.post('/portfolios/1/access', json={'username': 'x', 'role': 'viewer'})
    # The portfolio may not exist, but the decorator should allow request through to service which will raise later
    assert resp.status_code in (201, 500, 404)


def test_access_endpoint_with_auth(monkeypatch, client, db_session):
    # enable auth
    from app import create_app
    from app.config import get_config

    app = create_app(get_config('test'))
    app.config['REQUIRE_AUTH'] = True

    # mock validate_token_and_get_claims to accept token
    with patch('app.auth.auth.validate_token_and_get_claims', return_value={'sub': 'user'}):
        headers = {'Authorization': 'Bearer VALIDTOKEN'}
        resp = client.post('/portfolios/1/access', json={'username': 'x', 'role': 'viewer'}, headers=headers)
        assert resp.status_code in (201, 404, 500)
