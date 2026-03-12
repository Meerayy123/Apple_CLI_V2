from flask import Blueprint, jsonify, request

from app.db import db
from app.service import trade_service
from app.schemas import TradeOrderModel, SellOrderModel

trade_bp = Blueprint('trade', __name__)


@trade_bp.route('/buy', methods=['POST'])
def execute_purchase_order():
    req = TradeOrderModel(**request.get_json())
    trade_service.execute_purchase_order(portfolio_id=req.portfolio_id, ticker=req.ticker, quantity=req.quantity)
    db.session.commit()
    return jsonify({'message': 'Purchase order executed successfully'}), 201


@trade_bp.route('/sell', methods=['POST'])
def liquidate_investment():
    req = SellOrderModel(**request.get_json())
    trade_service.liquidate_investment(portfolio_id=req.portfolio_id, ticker=req.ticker, quantity=req.quantity, sale_price=req.sale_price)
    db.session.commit()
    return jsonify({'message': 'Investment liquidated successfully'}), 200
