import os


class Config(object):
    """Parent configuration class."""

    DEBUG = False
    SECRET_KEY = os.getenv("SECRET") or 'secret'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'postgresql:///spotify_sharing'
    SESSION_TYPE = 'filesystem'


class DevelopmentConfig(Config):
    """Configurations for development."""

    DEBUG = True
    DATABASE_URL = 'postgresql:///spotify_sharing'  # os.environ.get('DEV_DATABASE_URL')
    ENV= 'development'


class TestingConfig(Config):
    """Configurations for testing."""

    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql:///spotify_sharing_test' # os.environ.get('TEST_DATABASE_URL')
    ENV = 'testing'
    LOGIN_DISABLED = True # https://flask-login.readthedocs.io/en/latest/
    WTF_CSRF_ENABLED = False
    SESSION_COOKIE_DOMAIN = None
    PRESERVE_CONTEXT_ON_EXCEPTION = False # https://github.com/jarus/flask-testing/issues/21


class ProductionConfig(Config):
    """Configurations for production."""

    DEBUG = False
    if os.getenv("DATABASE_URL"):
        SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL").replace("://", "ql://", 1) # https://stackoverflow.com/questions/66690321/flask-and-heroku-sqlalchemy-exc-nosuchmoduleerror-cant-load-plugin-sqlalchemy
    ENV = 'production'


app_config = {
    'DEFAULT': DevelopmentConfig,
    'TESTING': TestingConfig,
    'PRODUCTION': ProductionConfig
}