from App.database import create_db
from App.controllers.user import create_user_basic

def initialize():
    create_db()

    seed = create_user_basic("bob", "bobpass", "DRIVER")

    return {"message": "database initialized", "seed": seed}