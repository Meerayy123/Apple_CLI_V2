from __future__ import annotations

from typing import List

from app.db import db


class Portfolio(db.Model):
    __tablename__ = 'portfolio'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    owner = db.Column(db.String(30), db.ForeignKey('user.username'), nullable=False)

    investments = db.relationship('Investment', back_populates='portfolio', lazy='selectin')

    user = db.relationship('User', foreign_keys=[owner], back_populates='portfolios', lazy='selectin')

    transactions = db.relationship('Transaction', back_populates='portfolio', lazy='selectin')

    def __str__(self):
        user_str = getattr(self, 'user', None)
        username = user_str.username if user_str else 'N/A'
        investments = []
        for investment in self.investments:
            investments.append(
                {
                    'ticker': investment.ticker,
                    'quantity': investment.quantity,
                }
            )
        return f'<Portfolio: id={self.id}; name={self.name}; description={self.description}; user={username}; investments={", ".join(investments)}>'

    def __to_dict__(self):
        investments = []
        for investment in self.investments:
            investments.append(
                {
                    'ticker': investment.ticker,
                    'quantity': investment.quantity,
                }
            )
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'owner': self.owner,
            'investments_count': len(self.investments),
            'investments': investments,
        }
