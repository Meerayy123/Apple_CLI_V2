import os
from unittest.mock import patch

import pytest

from app.services.alpha_vantage_client import get_company_name, get_price_data, get_quote


@pytest.fixture(autouse=True)
def set_api_key(monkeypatch):
    monkeypatch.setenv('ALPHAVANTAGE_API_KEY', 'TESTKEY')


def test_get_company_name_cached(monkeypatch):
    # mock requests.get to return a specific JSON
    class MockResp:
        def json(self):
            return {'Name': 'Test Corp'}

    with patch('app.services.alpha_vantage_client.requests.get', return_value=MockResp()):
        name = get_company_name('TEST')
        assert name == 'Test Corp'
        # second call should hit cache (no requests.get called again)
        name2 = get_company_name('TEST')
        assert name2 == 'Test Corp'


def test_get_price_data_and_quote(monkeypatch):
    class MockResp:
        def json(self):
            return {'Global Quote': {'05. price': '123.45'}}

    with patch('app.services.alpha_vantage_client.requests.get', return_value=MockResp()):
        pd = get_price_data('AAPL')
        assert pd is not None
        assert pd.get('05. price') == '123.45'
        q = get_quote('AAPL')
        assert q.price == 123.45
