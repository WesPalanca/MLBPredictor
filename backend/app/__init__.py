from flask import Flask
from .config import Config
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager


db = SQLAlchemy()
jwt = JWTManager()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)  
    db.init_app(app)
    jwt.init_app(app)
    CORS(app, resources={r"/api/*": {"origins": "http://localhost:5000"}})
    from .routes import register_blueprints
    with app.app_context(): # create tables
        db.create_all()
    register_blueprints(app)

    return app