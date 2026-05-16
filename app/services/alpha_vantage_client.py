import os
from dataclasses import dataclass
from typing import Optional, Dict, Any

import requests

from app import cache


@dataclass
class SecurityQuote:
    ticker: str
    company_name: Optional[str]
    price: Optional[float]


def _api_key() -> str:
    # prefer Flask config via environment variable; fall back to env
    return os.environ.get('ALPHAVANTAGE_API_KEY', '')


def _cache_key(kind: str, ticker: str) -> str:
    return f'alpha:{kind}:{ticker.upper()}'


def get_company_name(ticker: str) -> Optional[str]:
    key = _cache_key('company', ticker)
    cached = None
    try:
        cached = cache.get(key)
    except Exception:
        cached = None
    if cached:
        return cached

    api_key = _api_key()
    if not api_key:
        return None

    url = 'https://www.alphavantage.co/query'
    params = {'function': 'OVERVIEW', 'symbol': ticker, 'apikey': api_key}
    resp = requests.get(url, params=params, timeout=5)
    data = resp.json()
    name = data.get('Name') or data.get('CompanyName')
    if name:
        try:
            cache.set(key, name, timeout=60 * 60)
        except Exception:
            pass
    return name


def get_price_data(ticker: str) -> Optional[Dict[str, Any]]:
    key = _cache_key('price', ticker)
    try:
        cached = cache.get(key)
    except Exception:
        cached = None
    if cached:
        return cached

    api_key = _api_key()
    if not api_key:
        return None

    url = 'https://www.alphavantage.co/query'
    params = {'function': 'GLOBAL_QUOTE', 'symbol': ticker, 'apikey': api_key}
    resp = requests.get(url, params=params, timeout=5)
    data = resp.json()
    quote = data.get('Global Quote') or data.get('GlobalQuote')
    if quote and isinstance(quote, dict):
        try:
            cache.set(key, quote, timeout=60)
        except Exception:
            pass
        return quote
    return None


def get_quote(ticker: str) -> Optional[SecurityQuote]:
    # Try to use cached company and price values
    company = get_company_name(ticker)
    price_data = get_price_data(ticker)
    price = None
    if price_data:
        # AlphaVantage returns price under '05. price' or '05 price' variants
        price_str = price_data.get('05. price') or price_data.get('05 price') or price_data.get('price')
        try:
            price = float(price_str) if price_str is not None else None
        except Exception:
            price = None
    return SecurityQuote(ticker=ticker.upper(), company_name=company, price=price)
