from .user import bp as user_bp

blueprints = [user_bp]

def register_blueprints(app):
    for bp in blueprints:
        app.register_blueprint(bp)