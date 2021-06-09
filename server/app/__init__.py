from flask import Flask
from flask_cors import CORS
from flask_caching import Cache
from flask_jwt_extended import JWTManager

from app.authorization import AuthMiddleWare
from app.db import create_engine_and_session
from app.config import Config
from app.routes import register_blueprints
from database.data import setup_db

app = Flask(__name__)
CORS(app)
app.config.from_object(Config)
app.wsgi_app = AuthMiddleWare(app.wsgi_app)
jwt = JWTManager(app)

cache = Cache(app)

register_blueprints(app)
create_engine_and_session(app)
setup_db(app, cache)
