from typing import Optional

from app.db import db
from app.models import PortfolioAccess


class AccessError(Exception):
    pass


def grant_access(portfolio_id: int, username: str, role: str = 'viewer') -> int:
    if role not in ('viewer', 'manager'):
        raise AccessError('Invalid role')
    access = PortfolioAccess(portfolio_id=portfolio_id, username=username, role=role)
    try:
        db.session.add(access)
        db.session.flush()
        return access.id
    except Exception as e:
        # Let caller handle rollback/commit
        raise AccessError(str(e))


def revoke_access(access_id: int):
    access = db.session.query(PortfolioAccess).filter_by(id=access_id).one_or_none()
    if not access:
        raise AccessError('Access entry not found')
    try:
        db.session.delete(access)
        db.session.flush()
    except Exception as e:
        raise AccessError(str(e))


def get_access_for_portfolio(portfolio_id: int):
    try:
        return db.session.query(PortfolioAccess).filter_by(portfolio_id=portfolio_id).all()
    except Exception as e:
        raise AccessError(str(e))
