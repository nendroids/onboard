# ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
# ┃ backend: init                                                                                    ┃
# ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

from __future__ import annotations

from pathlib import Path

from backend.api.v1 import api_v1
from backend.config import Config
from backend.cli import register_db
from backend.utils.dirs import ensure_directories
from backend.extensions import (
    db,
    cache,
    cors,
    jwt,
    lm,
    mail,
    migrate,
    celery as celery_ext,
)
from backend.lib import make_celery
from backend.middleware import register_error_handlers

from flask import Flask, render_template

BASE_DIR = Path(__file__).resolve().parents[2]
FRONTEND = BASE_DIR.joinpath("frontend", "dist")


def create_app(config_class=None) -> Flask:
    app = Flask(
        __name__,
        instance_relative_config=True,
        static_folder=str(FRONTEND.joinpath("assets")),
        template_folder=str(FRONTEND),
    )

    ensure_directories()

    if config_class is None:
        app.config.from_object(Config)
    else:
        app.config.from_object(config_class)

    db.init_app(app)
    cache.init_app(app)
    cors.init_app(
        app,
        resources={r"/*": {"origins": app.config.get("FRONTEND_URL", "*")}},
        supports_credentials=True,
    )
    jwt.init_app(app)
    lm.init_app(app)
    lm.login_view = "auth.login"
    lm.login_message = "login required to access this page."
    lm.login_message_category = "info"

    @lm.user_loader
    def load_user(user_id: str) -> str:
        from backend.models import User

        return db.session.get(User, int(user_id))

    mail.init_app(app)
    migrate.init_app(app, db)
    make_celery(app, celery_ext)
    register_db(app)
    register_error_handlers(app)
    with app.app_context():
        db.create_all()

    app.register_blueprint(api_v1)

    @app.route("/")
    def index():
        return render_template("index.html")

    return app
