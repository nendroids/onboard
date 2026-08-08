# ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
# ┃ backend: extensions                                                                              ┃
# ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

from flask_caching import Cache
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from celery import Celery

db: SQLAlchemy = SQLAlchemy()
cache: Cache = Cache()
cors: CORS = CORS()
jwt: JWTManager = JWTManager()
lm: LoginManager = LoginManager()
mail: Mail = Mail()
migrate: Migrate = Migrate()
celery: Celery = Celery()
