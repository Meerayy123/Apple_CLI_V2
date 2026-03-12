import pytest

from app.models import User, Portfolio, Security
from app.service import portfolio_service


def test_get_users_route(client, db_session):
    user = User(username="routeuser", password="p", firstname="R", lastname="U", balance=100.0)
    db_session.add(user)
    db_session.commit()

    resp = client.get('/users/')
    assert resp.status_code == 200
    data = resp.get_json()
    assert any(u['username'] == 'routeuser' for u in data)


def test_create_user_route_and_error_handler(client, db_session):
    # successful creation
    payload = {
        'username': 'newuser',
        'password': 'pw',
        'firstname': 'New',
        'lastname': 'User',
        'balance': 50.0,
    }
    resp = client.post('/users/', json=payload)
    assert resp.status_code == 201

    # missing field triggers Pydantic validation -> 422
    bad_payload = {'password': 'x'}
    resp2 = client.post('/users/', json=bad_payload)
    assert resp2.status_code == 422
    data = resp2.get_json()
    assert data.get('error') == 'validation_error'


def test_portfolio_routes_create_and_get(client, db_session):
    user = User(username='pfuser', password='p', firstname='P', lastname='F', balance=200.0)
    db_session.add(user)
    db_session.commit()

    payload = {'username': 'pfuser', 'name': 'My PF', 'description': 'desc'}
    resp = client.post('/portfolios/', json=payload)
    assert resp.status_code == 201
    body = resp.get_json()
    pf_id = body.get('portfolio_id')
    assert pf_id is not None

    # fetch by id
    resp2 = client.get(f'/portfolios/{pf_id}')
    assert resp2.status_code == 200
    pf = resp2.get_json()
    assert pf['name'] == 'My PF'


def test_security_and_trade_routes(client, db_session):
    # securities seeded by db_session fixture
    resp = client.get('/securities/')
    assert resp.status_code == 200
    securities = resp.get_json()
    assert any(s['ticker'] == 'AAPL' for s in securities)

    # create user and portfolio to exercise trade buy/sell
    user = User(username='trader', password='p', firstname='T', lastname='R', balance=1000.0)
    db_session.add(user)
    db_session.commit()
    pf_id = portfolio_service.create_portfolio('Trade PF', 'for trades', user)
    db_session.commit()

    buy_payload = {'portfolio_id': pf_id, 'ticker': 'AAPL', 'quantity': 2}
    resp_buy = client.post('/trades/buy', json=buy_payload)
    assert resp_buy.status_code == 201

    # after buy, user's balance should have decreased
    updated_user = db_session.query(User).filter_by(username='trader').one()
    assert updated_user.balance == 1000.0 - (2 * 150.0)

    # sell (liquidate) the investment
    sell_payload = {'portfolio_id': pf_id, 'ticker': 'AAPL', 'quantity': 2, 'sale_price': 150.0}
    resp_sell = client.post('/trades/sell', json=sell_payload)
    assert resp_sell.status_code == 200
