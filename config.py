from information import *

HOME = "~/flask-demo"
PORT = 5001
APP_NAME = "flask-demo"


class Config:
    DEBUG = False
    TESTING = False
    API_TIMEOUT = 5

    def __init__(self):
        pass

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    HOME = "/flask-demo"
    ENV = "development"
    DEBUG = True
    TOKEN_SECRET = "token"
    SQLALCHEMY_DATABASE_URI = (
            "mysql+pymysql://"
            + DB_USER
            + ":"
            + DB_PASSWORD
            + "@"
            + DB_INSTANCE
            + "/"
            + DB_DATABASE
    )
    SECRET_KEY = "flask-demo"
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = "adityamaheshwari020@gmail.com"
    MAIL_PASSWORD = "evvzhkkbkbbxaspf"


config = {"development": DevelopmentConfig, "default": DevelopmentConfig}
