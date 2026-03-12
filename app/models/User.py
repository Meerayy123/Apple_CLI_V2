from __future__ import annotations

from typing import List

from app.db import db


class User(db.Model):
    __tablename__ = 'user'

    username = db.Column(db.String(30), primary_key=True)
    password = db.Column(db.String(30), nullable=False)
    firstname = db.Column(db.String(30), nullable=False)
    lastname = db.Column(db.String(30), nullable=False)
    balance = db.Column(db.Float, nullable=False)

    portfolios = db.relationship('Portfolio', back_populates='user', lazy='selectin')
    transactions = db.relationship('Transaction', back_populates='user', lazy='selectin')

    def __str__(self):
        return (
            f"<User: username='{self.username}'; "
            f"name='{self.firstname} {self.lastname}'; "
            f"#portfolios={len(self.portfolios)}; "
            f'balance={self.balance})'
        )

    def __to_dict__(self):
        return {
            'username': self.username,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'balance': self.balance,
        }
