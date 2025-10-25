from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()
__bound_app = None 

def init_db(app):
    global __bound_app
    __bound_app = app
    db.init_app(app)
    migrate.init_app(app, db)

def create_db():
    if __bound_app is None:
        raise RuntimeError("init_db(app) has not been called; no app is bound")
    with __bound_app.app_context():
        db.drop_all()
        db.create_all()

def drop_db():
    if __bound_app is None:
        raise RuntimeError("init_db(app) has not been called")
    with __bound_app.app_context():
        db.drop_all()