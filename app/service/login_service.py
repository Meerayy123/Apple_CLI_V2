from app.db import db
from app.models import User
from app.cli import session_state


class LoginError(Exception):
    pass


def login(username: str, password: str):
    user = db.session.query(User).filter_by(username=username).one_or_none()
    if not user or user.password != password:
        raise LoginError('Invalid username or password')
    session_state.set_logged_in_user(user)


def logout():
    session_state.clear_logged_in_user()
