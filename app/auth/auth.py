import os
import time
from typing import Dict, Any, Optional

import requests
try:
    from jose import jwt
except Exception:  # pragma: no cover - editor/runtime may not have python-jose
    jwt = None
from flask import current_app, g


def _get_cache():
    try:
        # lazy import to avoid circular app import at module load
        from app import cache as _cache
        return _cache
    except Exception:
        return None


class AuthError(Exception):
    pass


def _jwks_cache_key(url: str) -> str:
    return f'jwks:{url}'


def _fetch_jwks(jwks_url: str) -> Dict[str, Any]:
    key = _jwks_cache_key(jwks_url)
    cache = _get_cache()
    try:
        cached = cache.get(key) if cache is not None else None
    except Exception:
        cached = None
    if cached:
        return cached
    resp = requests.get(jwks_url, timeout=5)
    jwks = resp.json()
    cache = _get_cache()
    try:
        if cache is not None:
            cache.set(key, jwks, timeout=60 * 60)
    except Exception:
        pass
    return jwks


def validate_token_and_get_claims(token: str) -> Dict[str, Any]:
    # Read configuration from app config or env
    issuer = current_app.config.get('OIDC_ISSUER') or os.environ.get('OIDC_ISSUER')
    audience = current_app.config.get('OIDC_AUD') or os.environ.get('OIDC_AUD')
    jwks_url = current_app.config.get('OIDC_JWKS_URL') or os.environ.get('OIDC_JWKS_URL')
    if not jwks_url:
        raise AuthError('JWKS URL not configured')

    jwks = _fetch_jwks(jwks_url)
    try:
        # let jose find key automatically from JWKS
        if jwt is None:
            raise AuthError('JWT library not available')
        claims = jwt.decode(token, jwks, audience=audience, issuer=issuer)
        return claims
    except Exception as e:
        raise AuthError(str(e))


def require_auth(func):
    """Decorator for routes. Honors app.config['REQUIRE_AUTH'].

    If REQUIRE_AUTH is False, the decorator is a no-op and g.user is left unset.
    If True, validates Bearer token and sets g.user to token claims.
    """

    from functools import wraps
    from flask import request, jsonify

    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_app.config.get('REQUIRE_AUTH', False):
            # auth disabled
            return func(*args, **kwargs)

        auth = request.headers.get('Authorization', None)
        if not auth or not auth.startswith('Bearer '):
            return jsonify({'error': 'unauthorized'}), 401
        token = auth.split(' ', 1)[1]
        try:
            claims = validate_token_and_get_claims(token)
            g.user = claims
        except AuthError:
            return jsonify({'error': 'unauthorized'}), 401
        return func(*args, **kwargs)

    return wrapper
