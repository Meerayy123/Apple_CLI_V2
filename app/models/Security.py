from __future__ import annotations

from typing import List

from app.db import db


class Security(db.Model):
    __tablename__ = 'security'
    ticker = db.Column(db.String(10), primary_key=True)
    issuer = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)

    investments = db.relationship('Investment', back_populates='security', lazy='selectin')

    transactions = db.relationship('Transaction', back_populates='security', lazy='selectin')

    def __str__(self):
        return f'<Security: ticker={self.ticker}; issuer={self.issuer}; price={self.price}; #investments={len(self.investments)}>'

    def __to_dict__(self):
        return {
            'ticker': self.ticker,
            'issuer': self.issuer,
            'price': self.price,
        }
