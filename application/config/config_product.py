class ConfigProduct(object):
    SQLALCHEMY_DATABASE_URI = "postgresql://admin:123456abcA@localhost:5432/flask_tutorial"
    SECRET_KEY = 'e2q8dhaushdauwd7qye'
    SESSION_COOKIE_SALT = 'dhuasud819wubadhysagd'
    AUTH_EXPIRE_TIME = 86400
    TOKEN_EXPIRED = 86400
    STATIC_URL = "/static"