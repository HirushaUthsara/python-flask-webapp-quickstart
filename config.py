import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration class."""
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your_secret_key')  # Replace with a secure key in production
    COSMOS_ENDPOINT = os.environ.get('COSMOS_ENDPOINT')
    COSMOS_KEY = os.environ.get('COSMOS_KEY')
    COSMOS_DATABASE = os.environ.get('COSMOS_DATABASE', 'todosdb')
    COSMOS_CONTAINER = os.environ.get('COSMOS_CONTAINER', 'todos')

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True

class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    COSMOS_DATABASE = 'testtodosdb'
    COSMOS_CONTAINER = 'testtodos'

class ProductionConfig(Config):
    """Production configuration."""
    pass