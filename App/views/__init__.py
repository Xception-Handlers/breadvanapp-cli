# from .user import register as register_user
# from .schedule import register as register_schedule
# from .inbox import register as register_inbox
# from .request import register as register_request
# from .driver import register as register_driver

# def register_cli(app):
#     register_user(app)
#     register_schedule(app)
#     register_inbox(app)
#     register_request(app)
#     register_driver(app)

from .index import index_views
from .api import api
from .inbox import register as register_inbox_cli
from .schedule import register as register_schedule_cli
from .request import register as register_request_cli

def register_api(app):
    app.register_blueprint(index_views)
    app.register_blueprint(api)

def register_cli(app):
    register_inbox_cli(app)
    register_schedule_cli(app)
    register_request_cli(app)