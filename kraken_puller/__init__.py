from flask import Flask
from kraken_puller.config import Config


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    from kraken_puller.main.routes import main
    app.register_blueprint(main)
    return app
