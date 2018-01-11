import os 

#basedir = os.path.abspath(".")
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY="Hard to guess string"
    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    TEMPLATES_AUTO_RELOAD = True
    

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