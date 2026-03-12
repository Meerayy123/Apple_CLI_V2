from __future__ import annotations

from app.db import db


class Investment(db.Model):
    __tablename__ = 'investment'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    quantity = db.Column(db.Integer, nullable=False)
    ticker = db.Column(db.String(10), db.ForeignKey('security.ticker'))
    portfolio_id = db.Column(db.Integer, db.ForeignKey('portfolio.id'))

    security = db.relationship('Security', foreign_keys=[ticker], back_populates='investments', lazy='selectin')

    portfolio = db.relationship('Portfolio', foreign_keys=[portfolio_id], back_populates='investments', lazy='selectin')

    def __str__(self):
        return f'<Investment: id={self.id}; portfolio id={self.portfolio_id}; quantity={self.quantity}; portfolio={self.portfolio}>'
