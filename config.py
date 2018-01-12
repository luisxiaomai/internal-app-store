import os 

#basedir = os.path.abspath(".")
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY="Hard to guess string"
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    TEMPLATES_AUTO_RELOAD = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///"+os.path.join(basedir,"data-dev.sqlite")
    

class TestingConfig(Config):
    TESTING = True    

class ProductionConfig(Config):
    Production = True

config = {
    "development":DevelopmentConfig,
    "testing":TestingConfig,
    "productin":ProductionConfig,
    "default":DevelopmentConfig
}