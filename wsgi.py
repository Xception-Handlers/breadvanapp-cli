
from App.main import create_app
from App.database import db
from App.controllers import initialize

app = create_app()

@app.cli.command("init", help="Creates tables then seeds initial data")
def init_cmd():
    with app.app_context():
        db.create_all()  
        out = initialize()
        print(out.get("message", "database initialized"))
        if "seed" in out:
            print(out["seed"])

@app.cli.command("schema-reset", help="Drops ALL tables and recreates them")
def schema_reset():
    with app.app_context():
        db.drop_all()
        db.create_all()
        print("Schema dropped & recreated.")