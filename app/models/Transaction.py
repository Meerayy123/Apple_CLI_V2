import datetime

from app.db import db


class Transaction(db.Model):
    __tablename__ = 'transaction'
    transaction_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(30), db.ForeignKey('user.username'), nullable=False)
    portfolio_id = db.Column(db.Integer, db.ForeignKey('portfolio.id'), nullable=False)
    ticker = db.Column(db.String(30), db.ForeignKey('security.ticker'), nullable=False)
    transaction_type = db.Column(db.String(10), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    date_time = db.Column(db.DateTime, nullable=False)

    user = db.relationship('User', back_populates='transactions', foreign_keys=[username], lazy='selectin')
    portfolio = db.relationship('Portfolio', back_populates='transactions', foreign_keys=[portfolio_id], lazy='selectin')
    security = db.relationship('Security', back_populates='transactions', foreign_keys=[ticker], lazy='selectin')

    def __str__(self):
        return (
            f'<Transaction: id={self.transaction_id}; user={self.username}; '
            f'portfolio_id={self.portfolio_id}; ticker={self.ticker}; '
            f'type={self.transaction_type}; quantity={self.quantity}; '
            f'price={self.price}; date_time={self.date_time}>'
        )

    def __to_dict__(self):
        return {
            'transaction_id': self.transaction_id,
            'username': self.username,
            'portfolio_id': self.portfolio_id,
            'ticker': self.ticker,
            'transaction_type': self.transaction_type,
            'quantity': self.quantity,
            'price': self.price,
            'date_time': self.date_time.isoformat(),
        }
