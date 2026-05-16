from typing import List, Optional

from app.db import db
import app.database as database
from app.models import Security
from app.service import trade_service


class SecurityException(Exception):
    pass


def get_all_securities() -> List[Security]:
    session = None
    try:
        session = database.get_session()
        securities = session.query(Security).all()
        return securities
    except Exception as e:
        # Let caller handle rollback/commit
        raise SecurityException(f'Failed to retrieve securities due to error: {str(e)}')


def get_security_by_ticker(ticker: str) -> Optional[Security]:
    session = None
    try:
        session = database.get_session()
        security = session.query(Security).filter_by(ticker=ticker).one_or_none()
        return security
    except Exception as e:
        raise SecurityException(f'Failed to retrieve security due to error: {str(e)}')


# Backwards-compatible wrappers expected by tests
InsufficientFundsError = trade_service.InsufficientFundsError


def execute_purchase_order(portfolio_id: int, ticker: str, quantity: int):
    try:
        return trade_service.execute_purchase_order(portfolio_id, ticker, quantity)
    except trade_service.InsufficientFundsError:
        # Preserve the specific insufficient funds error for callers/tests
        raise
    except trade_service.TradeExecutionException as e:
        # Wrap other trade execution errors as SecurityException for the service API
        raise SecurityException(str(e))
