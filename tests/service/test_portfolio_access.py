import pytest

from app.models import User


def test_grant_and_revoke_access(client, db_session):
    user = User(username='accessuser', password='p', firstname='A', lastname='U', balance=100.0)
    db_session.add(user)
    db_session.commit()

    # create portfolio
    resp = client.post('/portfolios/', json={'username': 'accessuser', 'name': 'Acc PF', 'description': 'x'})
    assert resp.status_code == 201
    pf_id = resp.get_json()['portfolio_id']

    # grant access
    resp2 = client.post(f'/portfolios/{pf_id}/access', json={'username': 'accessuser', 'role': 'viewer'})
    assert resp2.status_code == 201
    access_id = resp2.get_json()['access_id']

    # revoke access
    resp3 = client.delete(f'/portfolios/{pf_id}/access/{access_id}')
    assert resp3.status_code == 200
