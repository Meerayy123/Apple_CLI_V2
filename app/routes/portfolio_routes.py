from flask import Blueprint, jsonify, request

import app.service.portfolio_service as portfolio_service
import app.service.transaction_service as transaction_service
import app.service.user_service as user_service
from app.db import db
from app.schemas import CreatePortfolioModel
from app.service.portfolio_access_service import grant_access, revoke_access, get_access_for_portfolio
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


@portfolio_bp.route('/<int:portfolio_id>/transactions', methods=['GET'])
def get_portfolio_transactions(portfolio_id):
    transactions = transaction_service.get_transactions_by_portfolio_id(portfolio_id)
    return jsonify([transaction.__to_dict__() for transaction in transactions]), 200


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
