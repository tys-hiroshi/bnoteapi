class BaseConfig(object):
    DEBUG = True
    TESTING = True


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    BSVCONTENTSERVER_MONGODB_USER = "bnoteuser"
    BSVCONTENTSERVER_MONGODB_PASS = "pallallp5"


class TestingConfig(BaseConfig):
    DEBUG = False
    TESTING = True