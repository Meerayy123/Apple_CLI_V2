"""Simple in-memory session state used by CLI tests."""
_logged_in_user = None


def set_logged_in_user(user):
    global _logged_in_user
    _logged_in_user = user


def get_logged_in_user():
    return _logged_in_user


def clear_logged_in_user():
    global _logged_in_user
    _logged_in_user = None
