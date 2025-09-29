from flask import Flask
from App.config import Config
from App.database import init_db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    init_db(app)
    from App import models  

    from App.views import register_cli
    register_cli(app)

    return app