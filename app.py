from flask import Flask
from .config import DevelopmentConfig, TestingConfig, ProductionConfig
from .api import api
from .utils.exceptions import NotFoundError

def create_app(config_name=None):
    """Creates and configures the Flask application."""
    app = Flask(__name__)

    if config_name == 'testing':
        app.config.from_object(TestingConfig)
    elif config_name == 'production':
        app.config.from_object(ProductionConfig)
    else:
        app.config.from_object(DevelopmentConfig)

    app.register_blueprint(api)

    @app.errorhandler(NotFoundError)
    def handle_not_found_error(error):
        """Handles NotFoundError exceptions."""
        return {'message': error.message}, 404

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)