from typing import List, Optional

from app.db import db
import app.database as database
from app.models import Portfolio, User, Investment
from app.service import trade_service


class UnsupportedPortfolioOperationError(Exception):
    pass


class PortfolioOperationError(Exception):
    pass


def create_portfolio(name: str, description: str, user: User) -> int:
    if not name or not description or not user:
        raise UnsupportedPortfolioOperationError(
            f'Invalid input[name:{name}, description: {description}, user: {user}]. Please try again.'
        )
    portfolio = Portfolio(name=name, description=description, user=user)
    session = None
    try:
        session = database.get_session()
        session.add(portfolio)
        session.flush()
        return portfolio.id
    except Exception as e:
        # Let the caller (route) handle rollback/commit. Preserve a clear domain error.
        raise PortfolioOperationError(f'Failed to create portfolio due to error: {str(e)}')


def get_portfolios_by_user(user: User) -> List[Portfolio]:
    session = None
    try:
        session = database.get_session()
        portfolios = session.query(Portfolio).filter_by(owner=user.username).all()
        return portfolios
    except Exception as e:
        raise PortfolioOperationError(f'Failed to retrieve portfolios due to error: {str(e)}')


def get_all_portfolios() -> List[Portfolio]:
    session = None
    try:
        session = database.get_session()
        portfolios = session.query(Portfolio).all()
        return portfolios
    except Exception as e:
        raise PortfolioOperationError(f'Failed to retrieve portfolios due to error: {str(e)}')


def get_portfolio_by_id(portfolio_id: int) -> Optional[Portfolio]:
    session = None
    try:
        session = database.get_session()
        portfolio = session.query(Portfolio).filter_by(id=portfolio_id).one_or_none()
        return portfolio
    except Exception as e:
        raise PortfolioOperationError(f'Failed to retrieve portfolio due to error: {str(e)}')


def delete_portfolio(portfolio_id: int):
    session = None
    try:
        session = database.get_session()
        portfolio = session.query(Portfolio).filter_by(id=portfolio_id).one_or_none()
        if not portfolio:
            raise UnsupportedPortfolioOperationError(f'Portfolio with id {portfolio_id} does not exist')
        session.delete(portfolio)
        session.flush()
    except Exception as e:
        # Bubble up the original exception to the caller; let route handle rollback.
        raise e
    # Removed internal rollback for tests that expect exceptions to bubble up

def get_holdings(portfolio_id: int) -> List[Investment]:
    from app.models import Investment
    session = None
    try:
        session = database.get_session()
        holdings = session.query(Investment).filter_by(portfolio_id=portfolio_id).all()
        return holdings
    except Exception as e:
        raise PortfolioOperationError(f'Failed to retrieve holdings due to error: {str(e)}')

def liquidate_investment(portfolio_id: int, ticker: str, quantity: int, sale_price: float):
    """Delegate liquidation to the trade service and let exceptions bubble up for the caller/tests."""
    return trade_service.liquidate_investment(portfolio_id, ticker, quantity, sale_price)


def liquidate_investment(portfolio_id: int, ticker: str, quantity: int, sale_price: float):
    # Delegate to trade_service and expose the specific error types
    try:
        return trade_service.liquidate_investment(portfolio_id, ticker, quantity, sale_price)
    except trade_service.TradeExecutionException as e:
        # Convert to local UnsupportedPortfolioOperationError for tests that expect it
        raise UnsupportedPortfolioOperationError(str(e))

