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

def test_get_my_portfolios(client, db_session):
    user = User(username='testme', password='p', firstname='T', lastname='M', balance=100.0)
    db_session.add(user)
    db_session.commit()
    pf_id = portfolio_service.create_portfolio('Me PF', 'desc', user)
    db_session.commit()

    resp = client.get('/portfolios/me', headers={'X-Test-User': 'testme'})
    assert resp.status_code == 200
    data = resp.get_json()
    assert len(data) >= 1
    assert data[0]['name'] == 'Me PF'

def test_get_my_portfolios_new_user(client, db_session):
    resp = client.get('/portfolios/me', headers={'X-Test-User': 'unknown_user'})
    assert resp.status_code == 200
    assert resp.get_json() == []

def test_portfolio_holdings_and_transactions_happy_path(client, db_session):
    user = User(username='holder', password='p', firstname='H', lastname='O', balance=1000.0)
    db_session.add(user)
    db_session.commit()
    pf_id = portfolio_service.create_portfolio('Hold PF', 'desc', user)
    db_session.commit()

    # Buy to create a holding and a transaction
    client.post('/trades/buy', json={'portfolio_id': pf_id, 'ticker': 'AAPL', 'quantity': 5})
    
    # Test holdings
    resp_h = client.get(f'/portfolios/{pf_id}/holdings', headers={'X-Test-User': 'holder'})
    assert resp_h.status_code == 200
    holdings = resp_h.get_json()
    assert len(holdings) == 1
    assert holdings[0]['ticker'] == 'AAPL'
    assert holdings[0]['quantity'] == 5

    # Test transactions
    resp_t = client.get(f'/portfolios/{pf_id}/transactions', headers={'X-Test-User': 'holder'})
    assert resp_t.status_code == 200
    transactions = resp_t.get_json()
    assert len(transactions) == 1
    assert transactions[0]['ticker'] == 'AAPL'
    assert transactions[0]['type'] == 'BUY'

def test_portfolio_endpoints_forbidden(client, db_session):
    user = User(username='owner', password='p', firstname='O', lastname='W', balance=1000.0)
    db_session.add(user)
    db_session.commit()
    pf_id = portfolio_service.create_portfolio('Secure PF', 'desc', user)
    db_session.commit()

    # Try to access with a different user
    resp_h = client.get(f'/portfolios/{pf_id}/holdings', headers={'X-Test-User': 'stranger'})
    assert resp_h.status_code == 403

    resp_t = client.get(f'/portfolios/{pf_id}/transactions', headers={'X-Test-User': 'stranger'})
    assert resp_t.status_code == 403

def test_portfolio_endpoints_not_found(client, db_session):
    # Try to access non-existent portfolio
    resp_h = client.get('/portfolios/9999/holdings', headers={'X-Test-User': 'testuser'})
    assert resp_h.status_code == 404

    resp_t = client.get('/portfolios/9999/transactions', headers={'X-Test-User': 'testuser'})
    assert resp_t.status_code == 404

def test_portfolio_endpoints_unauthorized(client):
    # Enable REQUIRE_AUTH to trigger 401
    client.application.config['REQUIRE_AUTH'] = True
    
    resp_me = client.get('/portfolios/me')
    assert resp_me.status_code == 401
    
    resp_h = client.get('/portfolios/1/holdings')
    assert resp_h.status_code == 401

    resp_t = client.get('/portfolios/1/transactions')
    assert resp_t.status_code == 401
    
    client.application.config['REQUIRE_AUTH'] = False

