# from flask import Flask
# from App.config import Config
# from App.database import init_db

# def create_app():
#     app = Flask(__name__)
#     app.config.from_object(Config)

#     init_db(app)
#     from App import models  

#     from App.views import register_cli
#     register_cli(app)

#     return app


from __future__ import annotations

from flask import Flask
from App.config import Config
from App.database import init_db

def create_app(config_overrides: dict | None = None):
    app = Flask(__name__)
    app.config.from_object(Config)

    app.config.setdefault("SQLALCHEMY_SESSION_OPTIONS", {"expire_on_commit": False})

    if config_overrides:
        merged = {"SQLALCHEMY_SESSION_OPTIONS": {"expire_on_commit": False}}
        merged.update(config_overrides)
        app.config.update(merged)

  
    init_db(app)
 
    from App import models  

    from App.controllers import setup_jwt, add_auth_header_normalizer, add_auth_context
    setup_jwt(app)
    add_auth_header_normalizer(app)
    add_auth_context(app)

    from App.views import register_api, register_cli
    register_api(app)
    register_cli(app)

    return app