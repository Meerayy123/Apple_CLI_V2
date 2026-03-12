from app.db import db


class PortfolioAccess(db.Model):
    __tablename__ = 'portfolio_access'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    portfolio_id = db.Column(db.Integer, db.ForeignKey('portfolio.id'), nullable=False)
    username = db.Column(db.String(30), db.ForeignKey('user.username'), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # e.g., 'viewer', 'manager'

    def __str__(self):
        return f'<PortfolioAccess: portfolio={self.portfolio_id}; user={self.username}; role={self.role}>'
