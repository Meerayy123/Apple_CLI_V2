from flask import Blueprint, jsonify, request, g, current_app

import app.service.portfolio_service as portfolio_service
import app.service.transaction_service as transaction_service
import app.service.user_service as user_service
from app.db import db
from app.schemas import CreatePortfolioModel
from app.service.portfolio_access_service import grant_access, revoke_access, get_access_for_portfolio, check_access
from app.auth.auth import require_auth

portfolio_bp = Blueprint('portfolio', __name__)


@portfolio_bp.route('/', methods=['GET'])
def get_all_portfolios():
    portfolios = portfolio_service.get_all_portfolios()
    return jsonify([portfolio.__to_dict__() for portfolio in portfolios]), 200


@portfolio_bp.route('/<int:portfolio_id>', methods=['GET'])
def get_portfolio(portfolio_id):
    portfolio = portfolio_service.get_portfolio_by_id(portfolio_id)
    if portfolio is None:
        return jsonify({'error': f'Portfolio {portfolio_id} not found'}), 404
    return jsonify(portfolio.__to_dict__()), 200


@portfolio_bp.route('/user/<username>', methods=['GET'])
def get_portfolios_by_user(username):
    user = user_service.get_user_by_username(username)
    if user is None:
        return jsonify({'error': f'User {username} not found'}), 404
    portfolios = portfolio_service.get_portfolios_by_user(user)
    return jsonify([portfolio.__to_dict__() for portfolio in portfolios]), 200


@portfolio_bp.route('/', methods=['POST'])
def create_portfolio():
    req = CreatePortfolioModel(**request.get_json())
    user = user_service.get_user_by_username(req.username)
    if user is None:
        return jsonify({'error': f'User {req.username} not found'}), 404
    portfolio_id = portfolio_service.create_portfolio(name=req.name, description=req.description, user=user)
    db.session.commit()
    return jsonify({'message': 'Portfolio created successfully', 'portfolio_id': portfolio_id}), 201


@portfolio_bp.route('/<int:portfolio_id>', methods=['DELETE'])
def delete_portfolio(portfolio_id):
    portfolio_service.delete_portfolio(portfolio_id)
    db.session.commit()
    return jsonify({'message': 'Portfolio deleted successfully'}), 200



@portfolio_bp.route('/<int:portfolio_id>/access', methods=['POST'])
@require_auth
def add_portfolio_access(portfolio_id):
    req = request.get_json()
    username = req.get('username')
    role = req.get('role', 'viewer')
    access_id = grant_access(portfolio_id, username, role)
    db.session.commit()
    return jsonify({'message': 'Access granted', 'access_id': access_id}), 201


@portfolio_bp.route('/<int:portfolio_id>/access/<int:access_id>', methods=['DELETE'])
@require_auth
def delete_portfolio_access(portfolio_id, access_id):
    revoke_access(access_id)
    db.session.commit()
    return jsonify({'message': 'Access revoked'}), 200

def _get_current_username():
    username = None
    if hasattr(g, 'user') and isinstance(g.user, dict):
        username = g.user.get('email') or g.user.get('cognito:username') or g.user.get('username')
    if not username and not current_app.config.get('REQUIRE_AUTH', False):
        # Fallback for tests when auth is disabled
        username = request.headers.get('X-Test-User') or request.args.get('username') or 'testuser'
    return username

@portfolio_bp.route('/me', methods=['GET'])
@require_auth
def get_my_portfolios():
    username = _get_current_username()
    if not username:
        return jsonify({'error': 'unauthorized'}), 401
    user = user_service.get_user_by_username(username)
    if user is None:
        return jsonify([]), 200
    portfolios = portfolio_service.get_portfolios_by_user(user)
    return jsonify([portfolio.__to_dict__() for portfolio in portfolios]), 200

@portfolio_bp.route('/<int:portfolio_id>/holdings', methods=['GET'])
@require_auth
def get_portfolio_holdings(portfolio_id):
    username = _get_current_username()
    if not username:
        return jsonify({'error': 'unauthorized'}), 401
    
    portfolio = portfolio_service.get_portfolio_by_id(portfolio_id)
    if portfolio is None:
        return jsonify({'error': f'Portfolio {portfolio_id} not found'}), 404
        
    if not check_access(portfolio_id, username):
        return jsonify({'error': 'Forbidden'}), 403
    
    holdings = portfolio_service.get_holdings(portfolio_id)
    return jsonify([h.__to_dict__() for h in holdings]), 200

@portfolio_bp.route('/<int:portfolio_id>/transactions', methods=['GET'])
@require_auth
def get_portfolio_transactions(portfolio_id):
    username = _get_current_username()
    if not username:
        return jsonify({'error': 'unauthorized'}), 401
    
    portfolio = portfolio_service.get_portfolio_by_id(portfolio_id)
    if portfolio is None:
        return jsonify({'error': f'Portfolio {portfolio_id} not found'}), 404
        
    if not check_access(portfolio_id, username):
        return jsonify({'error': 'Forbidden'}), 403
    
    transactions = transaction_service.get_transactions_by_portfolio_id(portfolio_id)
    # Order results by timestamp DESC
    transactions.sort(key=lambda t: t.date_time, reverse=True)
    return jsonify([t.__to_dict__() for t in transactions]), 200

