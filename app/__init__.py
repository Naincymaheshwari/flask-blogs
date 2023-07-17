from flask import Flask
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from config import config

db = SQLAlchemy()
ma = Marshmallow()
mail = Mail()

def initialize_db(app):
    db.init_app(app)
    ma.init_app(app)
    migrate = Migrate(app, db)
    mail = Mail(app)


def create_app(config_name):
    app = Flask(__name__)

    CORS(app, resources={r"/*": {"origins": "*"}})
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    initialize_db(app)

    from app.users.views import users_bp as users_router
    app.register_blueprint(users_router, url_prefix='/user')

    from app.blogs.views import blogs_bp as blogs_router
    app.register_blueprint(blogs_router, url_prefix='/blogs')

    from app.comments.views import comments_bp as comments_router
    app.register_blueprint(comments_router, url_prefix='/blog')

    from app.likes.views import bloglikes_bp as bloglikes_router
    app.register_blueprint(bloglikes_router, url_prefix='/bloglikes')

    return app
