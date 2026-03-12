from flask import Flask, jsonify
from pydantic import ValidationError

from app.db import db
from app.routes import portfolio_bp, security_bp, trade_bp, user_bp
try:
    from flask_caching import Cache  # type: ignore
except Exception:  # pragma: no cover - fallback for editors/environments without the package
    # Provide a minimal no-op Cache implementation so imports don't fail in IDEs
    class Cache:  # type: ignore
        def __init__(self, *_, **__):
            pass

        def init_app(self, app):
            return None


# application-wide cache instance (initialized in create_app)
cache = Cache()


def create_app(config):
    try:
        app = Flask(__name__)
        app.config.from_object(config)

        # register extensions
        db.init_app(app)
        cache.init_app(app)

        # register blueprints
        app.register_blueprint(user_bp, url_prefix='/users')
        app.register_blueprint(portfolio_bp, url_prefix='/portfolios')
        app.register_blueprint(security_bp, url_prefix='/securities')
        app.register_blueprint(trade_bp, url_prefix='/trades')

        # centralized Pydantic validation error handler
        @app.errorhandler(ValidationError)
        def handle_validation_error(err):
            # Pydantic v2 ValidationError provides .errors()
            detail = getattr(err, 'errors', None)
            try:
                detail = err.errors()
            except Exception:
                detail = str(err)
            return jsonify({'error': 'validation_error', 'detail': detail}), 422

        # centralized generic error handler that ensures transaction rollback
        @app.errorhandler(Exception)
        def handle_generic_exception(err):
            try:
                db.session.rollback()
            except Exception:
                pass
            return jsonify({'error': 'internal_server_error', 'detail': str(err)}), 500

        return app
    except Exception as e:
        print(f'Error creating app: {e}')
        raise
