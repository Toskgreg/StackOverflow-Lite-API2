
class Config(object):
    """Parent configuration class."""
    DEBUG = False
    DATABASE_URL = 'postgresql://postgres:andela@localhost:5432/question_db'


class DevelopmentConfiguration(Config):
    """Configurations for Development."""
    DEBUG = True


class TestingConfiguration(Config):
    """Configurations for Testing."""
    TESTING = True
    DEBUG = True
    DATABASE_URL = 'postgresql://postgres:andela@localhost:5432/test_db'


class ProductionConfiguration(Config):
    """Configurations for Production."""
    DEBUG = False
    DATABASE_URL = 'postgres://sxeryejnkxvdyl:fe0c442231427f6b1874f34a2608f09568dcbf48d4a65c22af4e5697a769761f@ec2-54-235-242-63.compute-1.amazonaws.com:5432/df6pburvodvkqn'


app_config = {
    'DEFAULT': DevelopmentConfiguration,
    'TESTING': TestingConfiguration,
    'DEVELOPMENT': DevelopmentConfiguration,
    'PRODUCTION': ProductionConfiguration
}
