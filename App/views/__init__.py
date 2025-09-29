from .user import register as register_user
from .schedule import register as register_schedule
from .inbox import register as register_inbox
from .request import register as register_request
from .driver import register as register_driver

def register_cli(app):
    register_user(app)
    register_schedule(app)
    register_inbox(app)
    register_request(app)
    register_driver(app)