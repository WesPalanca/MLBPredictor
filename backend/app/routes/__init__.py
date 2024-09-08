from .user import bp as user_bp
from .predict import bp as predict_bp

blueprints = [user_bp, predict_bp]

def register_blueprints(app):
    for bp in blueprints:
        app.register_blueprint(bp)